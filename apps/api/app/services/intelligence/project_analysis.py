from sqlalchemy.orm import Session
from app.models.government_project import GovernmentProject
from app.schemas.intelligence import (
    ProjectMetrics,
    ProjectEffectivenessCategory,
    ProjectEffectivenessResponse
)


def compute_project_metrics(db: Session, region_id: int) -> ProjectMetrics:
    projects = db.query(GovernmentProject).filter(GovernmentProject.region_id == region_id).all()
    
    total = len(projects)
    if total == 0:
        return ProjectMetrics(
            total_projects=0,
            planned=0,
            ongoing=0,
            completed=0,
            cancelled=0,
            total_budget=0.0
        )
    
    planned = sum(1 for p in projects if p.status.lower() in ["planned", "proposed"])
    ongoing = sum(1 for p in projects if p.status.lower() in ["ongoing", "in_progress", "in progress"])
    completed = sum(1 for p in projects if p.status.lower() in ["completed", "done", "finished"])
    cancelled = sum(1 for p in projects if p.status.lower() in ["cancelled", "halted", "suspended"])
    
    total_budget = sum(p.budget for p in projects if p.budget is not None)
    
    return ProjectMetrics(
        total_projects=total,
        planned=planned,
        ongoing=ongoing,
        completed=completed,
        cancelled=cancelled,
        total_budget=round(total_budget, 2)
    )


def compute_project_effectiveness(db: Session, region_id: int, region_name: str) -> ProjectEffectivenessResponse:
    projects = db.query(GovernmentProject).filter(GovernmentProject.region_id == region_id).all()
    
    status_breakdown = {
        "planned": 0,
        "ongoing": 0,
        "completed": 0,
        "cancelled": 0
    }
    
    category_map: dict[str, list[GovernmentProject]] = {}
    for p in projects:
        st = p.status.lower()
        if st in ["planned", "proposed"]:
            status_breakdown["planned"] += 1
        elif st in ["ongoing", "in_progress", "in progress"]:
            status_breakdown["ongoing"] += 1
        elif st in ["completed", "done", "finished"]:
            status_breakdown["completed"] += 1
        else:
            status_breakdown["cancelled"] += 1
            
        cat = p.category or "General"
        if cat not in category_map:
            category_map[cat] = []
        category_map[cat].append(p)
        
    category_list: list[ProjectEffectivenessCategory] = []
    for cat, item_list in category_map.items():
        c_planned = sum(1 for p in item_list if p.status.lower() in ["planned", "proposed"])
        c_ongoing = sum(1 for p in item_list if p.status.lower() in ["ongoing", "in_progress", "in progress"])
        c_completed = sum(1 for p in item_list if p.status.lower() in ["completed", "done", "finished"])
        c_cancelled = sum(1 for p in item_list if p.status.lower() in ["cancelled", "halted", "suspended"])
        c_budget = sum(p.budget for p in item_list if p.budget is not None)
        
        category_list.append(
            ProjectEffectivenessCategory(
                category=cat,
                total_projects=len(item_list),
                planned=c_planned,
                ongoing=c_ongoing,
                completed=c_completed,
                cancelled=c_cancelled,
                total_budget=round(c_budget, 2)
            )
        )
        
    return ProjectEffectivenessResponse(
        region_id=region_id,
        region_name=region_name,
        total_projects=len(projects),
        status_breakdown=status_breakdown,
        category_alignment=category_list
    )
