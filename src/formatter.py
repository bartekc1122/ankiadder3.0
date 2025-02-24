import json
from typing import Tuple, List
import logging

log = logging.getLogger(__name__)


class Formatter:
    def format_value(self, value) -> str:
        if isinstance(value, dict):
            return "\n".join(f"• {k}: {v}" for k, v in value.items())
        elif isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return str(value)

    def get_formatted_text(self, json_str: str) -> List[Tuple[str, str]]:
        log.debug(f"json str:{json_str}")
        if not isinstance(json_str, str):
            raise TypeError("Expected json_str to be a string.")

        json_str = self.check_json(json_str)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")

        if not isinstance(data, dict):
            raise ValueError("JSON does not represent a dictionary object.")
        formatted_parts: List[Tuple[str, str]] = []

        for key in data.keys():
            value = data[key]
            formatted_value = self.format_value(value)
            formatted_parts.append((key, formatted_value))

        log.debug(f"formatted parts: {formatted_parts}")
        return formatted_parts

    def check_json(self, json_str: str) -> str:
        if json_str.strip().startswith("{") and json_str.strip().endswith("}"):
            log.info("JSON is valid and properly formatted.")
            return json_str.strip()

        log.warning(
            f"Received malformed JSON - attempting to extract valid JSON object! json_str: {json_str}"
        )

        start_index = json_str.find("{")
        if start_index == -1:
            log.error("No opening brace found in the string!")
            return json_str

        end_index = json_str.rfind("}")
        if end_index == -1:
            log.error("No closing brave found in the string!")
            return json_str

        if end_index <= start_index:
            log.error(
                "JSON structure is invalid - closing brace appears before opening brace!"
            )
            return json_str

        trimmed_json = json_str[start_index : end_index + 1]

        if start_index > 0:
            log.info(f"Trimmed {start_index} characters from the beginning.")

        if end_index < len(json_str) - 1:
            log.info(
                f"Trimmed {len(json_str) - end_index - 1} characters from the end."
            )

        return trimmed_json
