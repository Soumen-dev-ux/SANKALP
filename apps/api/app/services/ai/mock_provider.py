from app.services.ai.base import CitizenUnderstanding


class MockAIProvider:

    def understand(
        self,
        text: str,
    ) -> CitizenUnderstanding:

        text_lower = text.lower()

        language = self.detect_language(text)

        category = "Other"
        issue = "General Development Issue"

        # -------------------------
        # WATER & SANITATION
        # -------------------------

        if any(
            word in text_lower
            for word in [
                "water",
                "drinking water",
                "toilet",
                "sanitation",
                "জল",
                "পানীয় জল",
                "পানীয় জল",
                "শৌচালয়",
                "শৌচালয়",
                "पानी",
                "पीने का पानी",
                "शौचालय",
            ]
        ):
            category = "Water & Sanitation"
            issue = "Drinking Water"

        # -------------------------
        # HEALTHCARE
        # -------------------------

        elif any(
            word in text_lower
            for word in [
                "hospital",
                "clinic",
                "doctor",
                "health",
                "হাসপাতাল",
                "ডাক্তার",
                "স্বাস্থ্য",
                "अस्पताल",
                "डॉक्टर",
                "स्वास्थ्य",
            ]
        ):
            category = "Healthcare"
            issue = "Healthcare Facility"

        # -------------------------
        # TRANSPORT
        # -------------------------

        elif any(
            word in text_lower
            for word in [
                "road",
                "traffic",
                "bus",
                "transport",
                "রাস্তা",
                "যানজট",
                "বাস",
                "পরিবহন",
                "सड़क",
                "ट्रैफिक",
                "बस",
                "परिवहन",
            ]
        ):
            category = "Transport"
            issue = "Transport Infrastructure"

        # -------------------------
        # EDUCATION
        # -------------------------

        elif any(
            word in text_lower
            for word in [
                "school",
                "college",
                "teacher",
                "education",
                "স্কুল",
                "কলেজ",
                "শিক্ষক",
                "শিক্ষা",
                "स्कूल",
                "कॉलेज",
                "शिक्षक",
                "शिक्षा",
            ]
        ):
            category = "Education"
            issue = "Education Facility"

        # -------------------------
        # DIGITAL CONNECTIVITY
        # -------------------------

        elif any(
            word in text_lower
            for word in [
                "internet",
                "network",
                "connectivity",
                "ইন্টারনেট",
                "নেটওয়ার্ক",
                "নেটওয়ার্ক",
                "সংযোগ",
                "इंटरनेट",
                "नेटवर्क",
                "कनेक्टिविटी",
            ]
        ):
            category = "Digital Connectivity"
            issue = "Digital Connectivity"

        return CitizenUnderstanding(
            language=language,
            category=category,
            intent="Report Development Need",
            issue=issue,
            location_text=self.extract_location(text),
        )

    # -------------------------
    # LANGUAGE DETECTION
    # -------------------------

    def detect_language(self, text: str) -> str:

        for char in text:

            # Bengali Unicode block
            if "\u0980" <= char <= "\u09ff":
                return "bn"

            # Devanagari Unicode block
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
            ("हमारे गांव में", "हमारे इलाके में"),
            ("हमारे गाँव में", "हमारे इलाके में"),
            ("हमारे इलाके में", "हमारे इलाके में"),
            ("हमारे शहर में", "हमारे शहर में"),
            ("हमारे वार्ड में", "हमारे वार्ड में"),
        ]

        for pattern, extracted in location_patterns:
            if pattern in text_lower:
                return extracted

        location_keywords = [
            "village",
            "town",
            "city",
            "ward",
            "area",
            "near",
            "district",
            "locality",
            "গ্রাম",
            "শহর",
            "এলাকা",
            "ওয়ার্ড",
            "ওয়ার্ড",
            "জেলা",
            "কাছে",
            "गांव",
            "शहर",
            "इलाका",
            "वार्ड",
            "जिला",
            "पास",
        ]

        for keyword in location_keywords:
            if keyword in text_lower:
                return text.strip()

        return None 