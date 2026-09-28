import re
from app.schemas.confidence import UnderstandingConfidence
from app.services.ai.base import CitizenUnderstanding
from app.schemas.ai_understanding import StructuredCitizenUnderstanding
from app.schemas.location import LocationEntity
from app.services.ai.normalizer import normalize_understanding
from app.services.ai.confidence import make_confidence


class MockAIProvider:

    def understand(
        self,
        text: str,
    ) -> CitizenUnderstanding:

        text_lower = text.lower()
        language = self.detect_language(text)

        category = "Other"
        issue = "General Development Issue"

        # WATER & SANITATION
        if any(
            word in text_lower
            for word in [
                "water", "drinking water", "toilet", "sanitation",
                "জল", "পানীয় জল", "পানীয় জল", "শৌচালয়", "শৌচালয়",
                "पानी", "पीने का पानी", "शौचालय",
            ]
        ):
            category = "Water & Sanitation"
            issue = "Drinking Water"

        # HEALTHCARE
        elif any(
            word in text_lower
            for word in [
                "hospital", "clinic", "doctor", "health",
                "হাসপাতাল", "ডাক্তার", "স্বাস্থ্য",
                "अस्पताल", "डॉक्टर", "स्वास्थ्य",
            ]
        ):
            category = "Healthcare"
            issue = "Healthcare Facility"

        # TRANSPORT
        elif any(
            word in text_lower
            for word in [
                "road", "traffic", "bus", "transport",
                "রাস্তা", "যানজট", "বাস", "পরিবহন",
                "सड़क", "ट्रैफिक", "बस", "परिवहन",
            ]
        ):
            category = "Transport"
            issue = "Transport Infrastructure"

        # EDUCATION
        elif any(
            word in text_lower
            for word in [
                "school", "college", "teacher", "education",
                "স্কুল", "কলেজ", "শিক্ষক", "শিক্ষা",
                "स्कूल", "कॉलेज", "शिक्षक", "शिक्षा",
            ]
        ):
            category = "Education"
            issue = "Education Facility"

        # DIGITAL CONNECTIVITY
        elif any(
            word in text_lower
            for word in [
                "internet", "network", "connectivity",
                "ইন্টারনেট", "নেটওয়ার্ক", "নেটওয়ার্ক", "সংযোগ",
                "इंटरनेट", "नेटवर्क", "कनेक्टिविटी",
            ]
        ):
            category = "Digital Connectivity"
            issue = "Digital Connectivity"

        intent = "Report Development Need"
        location_text = self.extract_location(text)
        location_type = "unknown"

        if location_text:
            loc_lower = location_text.lower()
            if any(w in loc_lower for w in ["village", "গ্রাম", "गांव", "गाँव"]):
                location_type = "village"
            elif any(w in loc_lower for w in ["town", "city", "শহর", "शहर"]):
                location_type = "town"
            elif any(w in loc_lower for w in ["ward", "ওয়ার্ড", "ওয়ার্ড", "वार्ड"]):
                location_type = "ward"
            elif any(w in loc_lower for w in ["area", "locality", "এলাকা", "इलाका", "इलाके"]):
                location_type = "area"
            elif any(w in loc_lower for w in ["district", "জেলা", "जिला"]):
                location_type = "district"
            else:
                location_type = "locality"

        # Generic phrases (e.g. "in our village") leave name as None, specific names populate name
        location_name = (
            None
            if (not location_text or any(gen in location_text.lower() for gen in ["our village", "our town", "our area", "our locality"]))
            else location_text
        )

        location = LocationEntity(
            text=location_text,
            type=location_type,
            name=location_name,
            ward=None,
            district=None,
            landmark=None,
        )

        confidence = UnderstandingConfidence(
            language=make_confidence(
                0.99,
                "Language explicitly identified from the request."
            ),
            category=make_confidence(
                0.95,
                f"Categorized as {category} based on keywords."
            ),
            intent=make_confidence(
                0.92,
                "The citizen is reporting a development need."
            ),
            issue=make_confidence(
                0.94,
                f"Identified issue: {issue}"
            ),
            location=make_confidence(
                0.90 if location_text else 0.50,
                "Location context extracted from input." if location_text else "General area assumed."
            ),
            overall_score=0.94 if location_text else 0.75,
            review_required=False,
        )

        structured = StructuredCitizenUnderstanding(
            language=language or "other",
            category=category or "Other",
            intent=intent or "Report Development Need",
            issue=issue or "General Development Issue",
            location=location,
            confidence=confidence,
        )

        return normalize_understanding(structured)

    def detect_language(self, text: str) -> str:
        for char in text:
            if "\u0980" <= char <= "\u09ff":
                return "bn"
            if "\u0900" <= char <= "\u097f":
                return "hi"
        return "en"

    def extract_location(self, text: str) -> str | None:
        text_lower = text.lower()

        location_patterns = [
            ("in our village", "in our village"),
            ("in our town", "in our town"),
            ("in our area", "in our area"),
            ("in our locality", "in our locality"),
            ("near our village", "near our village"),
            ("near our town", "near our town"),
            ("near our area", "near our area"),
            ("আমাদের গ্রামে", "আমাদের গ্রামে"),
            ("আমাদের এলাকায়", "আমাদের এলাকায়"),
            ("আমাদের এলাকায়", "আমাদের এলাকায়"),
            ("আমাদের শহরে", "আমাদের শহরে"),
            ("আমাদের ওয়ার্ডে", "আমাদের ওয়ার্ডে"),
            ("हमारे गांव में", "हमारे गांव में"),
            ("हमारे गाँव में", "हमारे गाँव में"),
            ("हमारे इलाके में", "हमारे इलाके में"),
            ("हमारे शहर में", "हमारे शहर में"),
            ("हमारे वार्ड में", "हमारे वार्ड में"),
        ]

        for pattern, extracted in location_patterns:
            if pattern in text_lower:
                return extracted

        prep_match = re.search(r'\b(?:in|at|near|around|from)\s+([A-Za-z0-9\s,-]+)', text, re.IGNORECASE)
        if prep_match:
            loc_str = prep_match.group(1).strip()
            if 0 < len(loc_str) < 100:
                return loc_str

        location_keywords = [
            "village", "town", "city", "ward", "area", "near", "district", "locality",
            "sector", "block", "panchayat", "colony", "nagar", "road", "street",
            "গ্রাম", "শহর", "এলাকা", "ওয়ার্ড", "ওয়ার্ড", "জেলা", "কাছে",
            "गांव", "शहर", "इलाका", "वार्ड", "जिला", "पास"
        ]

        for keyword in location_keywords:
            if keyword in text_lower:
                return text.strip()

        return None