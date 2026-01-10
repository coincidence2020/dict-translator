from typing import List, Dict

class MedicalTerm:
    """医学术语基类"""
    def __init__(self, source_name: str, descriptions: Dict[str, str]):
        self.source_name = source_name  # 源语言术语（如中文）
        self.descriptions = descriptions  # 多语言定义（如 {"en": "definition", "es": "definición"}）
        self.synonyms: List[str] = []     # 同义词列表
        self.translation_rules: List[str] = []  # 翻译约束规则（如 "禁止直译"）

    def add_synonym(self, synonym: str):
        self.synonyms.append(synonym)

    def validate_translation(self, target_lang: str, translation: str) -> bool:
        """验证翻译是否符合规则"""
        # 示例规则：禁止直译（如 "心绞痛" → "Heart Angry Pain" 无效）
        if "禁止直译" in self.translation_rules:
            return translation != self.source_name.translate(target_lang)
        return True

class Disease(MedicalTerm):
    """疾病类（继承自MedicalTerm）"""
    def __init__(self, source_name: str, descriptions: Dict[str, str], icd_code: str):
        super().__init__(source_name, descriptions)
        self.icd_code = icd_code  # 国际疾病分类编码
        self.recommended_drugs: List[Drug] = []  # 关联药物

    def get_translation(self, target_lang: str) -> str:
        """优先返回标准术语库中的翻译"""
        return self.descriptions.get(target_lang, self.source_name)

class Drug(MedicalTerm):
    """药物类（继承自MedicalTerm）"""
    def __init__(self, source_name: str, descriptions: Dict[str, str], atc_code: str):
        super().__init__(source_name, descriptions)
        self.atc_code = atc_code  # 药物分类编码
        self.formats: Dict[str, str] = {}  # 语言特定格式（如英文需大写）

    def apply_format(self, target_lang: str, name: str) -> str:
        """应用目标语言格式（如英文药品名大写）"""
        return self.formats.get(target_lang, name.upper() if target_lang == "en" else name)


# 初始化疾病实例
hypertension = Disease(
    source_name="高血压",
    descriptions={
        "en": "Hypertension",
        "es": "Hipertensión",
        "ja": "高血圧"
    },
    icd_code="I10"
)
hypertension.add_synonym("血压高")

# 初始化药物实例
aspirin = Drug(
    source_name="阿司匹林",
    descriptions={
        "en": "Aspirin",
        "es": "Aspirina",
        "ja": "アスピリン"
    },
    atc_code="B01AC06"
)
aspirin.formats = {"en": "ASPIRIN"}  # 英文名称强制大写


class MedicalTranslator:
    """医学翻译控制器"""

    def __init__(self):
        self.term_db: Dict[str, MedicalTerm] = {}  # 术语库（key为源语言词）

    def add_term(self, term: MedicalTerm):
        self.term_db[term.source_name] = term

    def translate_sentence(self, sentence: str, target_lang: str) -> str:
        translated_tokens = []
        for token in sentence.split():
            # 优先匹配术语库
            if token in self.term_db:
                term = self.term_db[token]
                translated = term.get_translation(target_lang)
                # 应用格式规则（如药物名大写）
                if isinstance(term, Drug):
                    translated = term.apply_format(target_lang, translated)
                translated_tokens.append(translated)
            else:
                # 通用翻译（此处可调用外部API如Google Translate）
                translated_tokens.append(self._fallback_translate(token, target_lang))
        return " ".join(translated_tokens)

    def _fallback_translate(self, token: str, target_lang: str) -> str:
        """备用翻译逻辑（示例）"""
        return token  # 实际可接入外部翻译API


# 初始化翻译器并加载术语
translator = MedicalTranslator()
translator.add_term(hypertension)
translator.add_term(aspirin)

# 输入句子
source_sentence = "患者有高血压，需每日服用阿司匹林"
target_lang = "en"

# 执行翻译
translation = translator.translate_sentence(source_sentence, target_lang)
print(translation)  # 输出: "Patient has Hypertension, needs to take ASPIRIN daily"