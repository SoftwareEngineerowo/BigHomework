from erniebot_agent.tools.base import Tool

from erniebot_agent.tools.schema import ToolParameterView

functions = [
    {
        "name": "get_current_score",
        "description": "获取指定学生指定科目最近的考试分数",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "学生姓名",
                },
                "subject": {
                    "type": "string",
                    "description": "考试科目"
                },
            },
            "required": ["name", "subject"]
        },
        "response": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "学生姓名",
                },
                "subject": {
                    "type": "string",
                    "description": "考试科目"
                },
                "scores": {
                    "type": "string",
                    "description": "考试分数"
                },
            },
        },
    },
]


def get_current_score(name: str, subject: str) -> dict:
    return {"name": name, "subject": subject, "scores": "121"}
