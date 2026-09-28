from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.region import Region
from app.models.citizen_request import CitizenRequest
from app.models.infrastructure import Infrastructure
from app.models.government_project import GovernmentProject
from app.schemas.intelligence import (
    RegionalIntelligenceResponse,
    DevelopmentSignal,
    DataQualitySummary,
    MultiRegionCompareResponse,
    RegionCompareMetrics,
    NeedVsDevelopmentResponse,
    NeedVsDevelopmentCategory,
    AIExplanationRequest,
    AIExplanationResponse
)
from app.services.intelligence.demand_analysis import compute_request_metrics
from app.services.intelligence.infrastructure_analysis import compute_infrastructure_metrics
from app.services.intelligence.project_analysis import compute_project_metrics
from app.services.ai.provider import get_ai_provider


class RegionalIntelligenceService:

    @staticmethod
    def get_regional_intelligence(db: Session, region_id: int) -> RegionalIntelligenceResponse:
        region = db.query(Region).filter(Region.id == region_id).first()
        if not region:
            raise ValueError(f"Region {region_id} not found")
            
        req_metrics = compute_request_metrics(db, region_id)
        infra_metrics = compute_infrastructure_metrics(db, region_id)
        proj_metrics = compute_project_metrics(db, region_id)
        
        # Calculate Development Signals across categories
        all_categories = set(c.category for c in req_metrics.categories)
        infra_records = db.query(Infrastructure).filter(Infrastructure.region_id == region_id).all()
        proj_records = db.query(GovernmentProject).filter(GovernmentProject.region_id == region_id).all()
        
        for i in infra_records:
            if i.category:
                all_categories.add(i.category)
        for p in proj_records:
            if p.category:
                all_categories.add(p.category)
                
        development_signals: list[DevelopmentSignal] = []
        warnings: list[str] = []
        
        if req_metrics.total_requests == 0:
            warnings.append("No citizen requests logged for this region.")
        if infra_metrics.total_units == 0:
            warnings.append("No infrastructure assets recorded for this region.")
        if proj_metrics.total_projects == 0:
            warnings.append("No government projects logged for this region.")
            
        for cat in sorted(all_categories):
            cat_reqs = sum(c.count for c in req_metrics.categories if c.category == cat)
            demand_score = round((cat_reqs / req_metrics.total_requests * 100.0), 1) if req_metrics.total_requests > 0 else 0.0
            
            cat_infra = [i for i in infra_records if i.category == cat]
            covs = [i.coverage_percent for i in cat_infra if i.coverage_percent is not None]
            quals = [i.quality_score for i in cat_infra if i.quality_score is not None]
            
            cat_coverage = round(sum(covs) / len(covs), 1) if covs else 0.0
            cat_quality = round(sum(quals) / len(quals), 2) if quals else 0.0
            
            # Transparent Gap Score: Demand Score - Infrastructure Coverage Score
            gap_score = round(max(0.0, demand_score - (cat_coverage * 0.5)), 1)
            
            cat_projects = sum(1 for p in proj_records if p.category == cat)
            
            cat_warnings = []
            if cat_reqs > 10 and cat_projects == 0:
                cat_warnings.append(f"High citizen demand ({cat_reqs} requests) with 0 active or planned projects.")
            if cat_infra and cat_coverage < 40.0:
                cat_warnings.append(f"Infrastructure coverage for {cat} is below critical threshold ({cat_coverage}%).")
                
            development_signals.append(
                DevelopmentSignal(
                    category=cat,
                    demand_score=demand_score,
                    infrastructure_coverage=cat_coverage,
                    infrastructure_quality=cat_quality,
                    gap_score=gap_score,
                    project_count=cat_projects,
                    data_warnings=cat_warnings
                )
            )
            
        return RegionalIntelligenceResponse(
            region_id=region.id,
            region_name=region.name,
            region_code=region.code,
            request_metrics=req_metrics,
            infrastructure_metrics=infra_metrics,
            project_metrics=proj_metrics,
            development_signals=development_signals,
            data_quality=DataQualitySummary(
                warnings=warnings,
                completeness_score=0.9 if warnings else 1.0
            )
        )

    @staticmethod
    def compare_regions(db: Session) -> MultiRegionCompareResponse:
        regions = db.query(Region).all()
        compare_list: list[RegionCompareMetrics] = []
        
        for r in regions:
            req_m = compute_request_metrics(db, r.id)
            inf_m = compute_infrastructure_metrics(db, r.id)
            prj_m = compute_project_metrics(db, r.id)
            
            top_cat = req_m.categories[0].category if req_m.categories else None
            
            compare_list.append(
                RegionCompareMetrics(
                    region_id=r.id,
                    region_name=r.name,
                    region_code=r.code,
                    total_requests=req_m.total_requests,
                    infrastructure_coverage=inf_m.average_coverage,
                    infrastructure_quality=inf_m.average_quality,
                    total_projects=prj_m.total_projects,
                    ongoing_projects=prj_m.ongoing,
                    top_demand_category=top_cat
                )
            )
            
        return MultiRegionCompareResponse(regions=compare_list)

    @staticmethod
    def analyze_need_vs_development(db: Session, region_id: int) -> NeedVsDevelopmentResponse:
        region = db.query(Region).filter(Region.id == region_id).first()
        if not region:
            raise ValueError(f"Region {region_id} not found")
            
        intel = RegionalIntelligenceService.get_regional_intelligence(db, region_id)
        categories: list[NeedVsDevelopmentCategory] = []
        
        for sig in intel.development_signals:
            cat_reqs = sum(c.count for c in intel.request_metrics.categories if c.category == sig.category)
            
            # Find projects in this category
            proj_records = db.query(GovernmentProject).filter(
                GovernmentProject.region_id == region_id,
                GovernmentProject.category == sig.category
            ).all()
            
            ongoing_cnt = sum(1 for p in proj_records if p.status.lower() in ["ongoing", "in_progress", "in progress"])
            
            misaligned = (sig.demand_score > 20.0 or cat_reqs >= 5) and len(proj_records) == 0
            
            if misaligned:
                status_summary = "CRITICAL GAP: High citizen demand with 0 government projects."
            elif ongoing_cnt > 0:
                status_summary = f"Active Development: {ongoing_cnt} ongoing project(s) addressing demand."
            elif len(proj_records) > 0:
                status_summary = f"Planned Development: {len(proj_records)} project(s) recorded."
            else:
                status_summary = "Stable: Low demand relative to current infrastructure capacity."
                
            categories.append(
                NeedVsDevelopmentCategory(
                    category=sig.category,
                    demand_volume=cat_reqs,
                    demand_share_percent=sig.demand_score,
                    infrastructure_coverage_percent=sig.infrastructure_coverage,
                    infrastructure_quality_score=sig.infrastructure_quality,
                    project_count=sig.project_count,
                    ongoing_project_count=ongoing_cnt,
                    misalignment_flag=misaligned,
                    status_summary=status_summary
                )
            )
            
        return NeedVsDevelopmentResponse(
            region_id=region.id,
            region_name=region.name,
            categories=categories
        )

    @staticmethod
    def generate_ai_explanation(db: Session, payload: AIExplanationRequest) -> AIExplanationResponse:
        region = db.query(Region).filter(Region.id == payload.region_id).first()
        if not region:
            raise ValueError(f"Region {payload.region_id} not found")
            
        intel = RegionalIntelligenceService.get_regional_intelligence(db, payload.region_id)
        
        # Formulate strict prompt backed by deterministic data
        prompt = (
            f"Analyze regional intelligence for {region.name} (Code: {region.code}).\n"
            f"Total Citizen Requests: {intel.request_metrics.total_requests}\n"
            f"Infrastructure Average Coverage: {intel.infrastructure_metrics.average_coverage}%, Quality: {intel.infrastructure_metrics.average_quality}\n"
            f"Projects: {intel.project_metrics.total_projects} (Ongoing: {intel.project_metrics.ongoing}, Planned: {intel.project_metrics.planned})\n"
            f"Development Signals: {[s.model_dump() for s in intel.development_signals]}\n"
            f"Data Quality Warnings: {intel.data_quality.warnings}\n"
            f"Provide structured evidence summary. DO NOT invent facts or change numbers."
        )
        
        ai_provider = get_ai_provider()
        raw_response = ai_provider.generate_response(prompt)
        
        # Build structured explanation backed by deterministic findings
        key_evidence = [
            f"{intel.request_metrics.total_requests} total citizen requests logged.",
            f"Average infrastructure coverage is {intel.infrastructure_metrics.average_coverage}% across {intel.infrastructure_metrics.total_units} recorded units.",
            f"{intel.project_metrics.total_projects} government projects recorded ({intel.project_metrics.ongoing} ongoing, {intel.project_metrics.planned} planned)."
        ]
        
        observed_trends = []
        if intel.request_metrics.categories:
            top_cat = intel.request_metrics.categories[0]
            observed_trends.append(f"Primary demand sector is '{top_cat.category}' accounting for {top_cat.percentage}% of citizen submissions.")
            
        limitations = intel.data_quality.warnings.copy()
        if not limitations:
            limitations.append("Analysis is constrained to logged citizen requests and registered government asset records.")
            
        questions = [
            "Do the logged citizen requests accurately reflect rural and under-connected sub-districts?",
            "Are planned infrastructure projects budgeted adequately to meet the observed category demand gap?",
            "Should non-operational infrastructure units be prioritized for repair before initiating new projects?"
        ]
        
        summary = (
            f"Regional Intelligence analysis for {region.name} indicates "
            f"{'high priority development gaps' if any(s.misalignment_flag for s in RegionalIntelligenceService.analyze_need_vs_development(db, region.id).categories) else 'balanced development progress'}. "
            f"{raw_response[:300] if raw_response else ''}"
        )
        
        return AIExplanationResponse(
            region_id=region.id,
            region_name=region.name,
            summary=summary,
            key_evidence=key_evidence,
            observed_trends=observed_trends,
            data_limitations=limitations,
            questions_for_human_review=questions
        )
