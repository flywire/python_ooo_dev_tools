from enum import Enum


class StyleParaKind(Enum):
    """Style Lookups for Paragraph Styles"""

    ADDRESSEE = "Addressee"
    APPENDIX = "Appendix"
    BIBLIOGRAPHY_1 = "Bibliography 1"
    BIBLIOGRAPHY_HEADING = "Bibliography Heading"
    CAPTION = "Caption"
    CONTENTS_1 = "Contents 1"
    CONTENTS_10 = "Contents 10"
    CONTENTS_2 = "Contents 2"
    CONTENTS_3 = "Contents 3"
    CONTENTS_4 = "Contents 4"
    CONTENTS_5 = "Contents 5"
    CONTENTS_6 = "Contents 6"
    CONTENTS_7 = "Contents 7"
    CONTENTS_8 = "Contents 8"
    CONTENTS_9 = "Contents 9"
    CONTENTS_HEADING = "Contents Heading"
    DRAWING = "Drawing"
    ENDNOTE = "Endnote"
    FIGURE = "Figure"
    FIGURE_INDEX_1 = "Figure Index 1"
    FIGURE_INDEX_HEADING = "Figure Index Heading"
    FIRST_LINE_INDENT = "First line indent"
    FOOTER = "Footer"
    FOOTER_LEFT = "Footer left"
    FOOTER_RIGHT = "Footer right"
    FOOTNOTE = "Footnote"
    FRAME_CONTENTS = "Frame contents"
    HANGING_INDENT = "Hanging indent"
    HEADER = "Header"
    HEADER_FOOTER = "Header and Footer"
    HEADER_LEFT = "Header left"
    HEADER_RIGHT = "Header right"
    HEADING = "Heading"
    HEADING_1 = "Heading 1"
    HEADING_10 = "Heading 10"
    HEADING_2 = "Heading 2"
    HEADING_3 = "Heading 3"
    HEADING_4 = "Heading 4"
    HEADING_5 = "Heading 5"
    HEADING_6 = "Heading 6"
    HEADING_7 = "Heading 7"
    HEADING_8 = "Heading 8"
    HEADING_9 = "Heading 9"
    HORIZONTAL_LINE = "Horizontal Line"
    ILLUSTRATION = "Illustration"
    INDEX = "Index"
    INDEX_1 = "Index 1"
    INDEX_2 = "Index 2"
    INDEX_3 = "Index 3"
    INDEX_HEADING = "Index Heading"
    INDEX_SEPARATOR = "Index Separator"
    LIST = "List"
    LIST_1 = "List 1"
    LIST_1_CONT = "List 1 Cont."
    LIST_1_END = "List 1 End"
    LIST_1_START = "List 1 Start"
    LIST_2 = "List 2"
    LIST_2_CONT = "List 2 Cont."
    LIST_2_END = "List 2 End"
    LIST_2_START = "List 2 Start"
    LIST_3 = "List 3"
    LIST_3_CONT = "List 3 Cont."
    LIST_3_END = "List 3 End"
    LIST_3_START = "List 3 Start"
    LIST_4 = "List 4"
    LIST_4_CONT = "List 4 Cont."
    LIST_4_END = "List 4 End"
    LIST_4_START = "List 4 Start"
    LIST_5 = "List 5"
    LIST_5_CONT = "List 5 Cont."
    LIST_5_END = "List 5 End"
    LIST_5_START = "List 5 Start"
    LIST_CONTENTS = "List Contents"
    LIST_HEADING = "List Heading"
    LIST_INDENT = "List Indent"
    NUMBERING_1 = "Numbering 1"
    NUMBERING_1_CONT = "Numbering 1 Cont."
    NUMBERING_1_END = "Numbering 1 End"
    NUMBERING_1_START = "Numbering 1 Start"
    NUMBERING_2 = "Numbering 2"
    NUMBERING_2_CONT = "Numbering 2 Cont."
    NUMBERING_2_END = "Numbering 2 End"
    NUMBERING_2_START = "Numbering 2 Start"
    NUMBERING_3 = "Numbering 3"
    NUMBERING_3_CONT = "Numbering 3 Cont."
    NUMBERING_3_END = "Numbering 3 End"
    NUMBERING_3_START = "Numbering 3 Start"
    NUMBERING_4 = "Numbering 4"
    NUMBERING_4_CONT = "Numbering 4 Cont."
    NUMBERING_4_END = "Numbering 4 End"
    NUMBERING_4_START = "Numbering 4 Start"
    NUMBERING_5 = "Numbering 5"
    NUMBERING_5_CONT = "Numbering 5 Cont."
    NUMBERING_5_END = "Numbering 5 End"
    NUMBERING_5_START = "Numbering 5 Start"
    MARGINALIA = "Marginalia"
    OBJECT_INDEX_1 = "Object index 1"
    OBJECT_INDEX_HEADING = "Object index heading"
    PREFORMATTED_TEXT = "Preformatted Text"
    QUOTATIONS = "Quotations"
    SALUTATION = "Salutation"
    SENDER = "Sender"
    SIGNATURE = "Signature"
    STANDARD = "Standard"
    SUBTITLE = "Subtitle"
    TABLE = "Table"
    TABLE_CONTENTS = "Table Contents"
    TABLE_HEADING = "Table Heading"
    TABLE_INDEX_1 = "Table index 1"
    TABLE_INDEX_HEADING = "Table index heading"
    TEXT = "Text"
    TEXT_BODY = "Text body"
    TEXT_BODY_INDENT = "Text body indent"
    TITLE = "Title"
    USER_INDEX_1 = "User Index 1"
    USER_INDEX_10 = "User Index 10"
    USER_INDEX_2 = "User Index 2"
    USER_INDEX_3 = "User Index 3"
    USER_INDEX_4 = "User Index 4"
    USER_INDEX_5 = "User Index 5"
    USER_INDEX_6 = "User Index 6"
    USER_INDEX_7 = "User Index 7"
    USER_INDEX_8 = "User Index 8"
    USER_INDEX_9 = "User Index 9"
    USER_INDEX_HEADING = "User Index Heading"

    def __str__(self) -> str:
        return self.value
