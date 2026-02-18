from pydantic import BaseModel, Field
from typing import Optional
import json

class User(BaseModel):
    id: int
    # 字段别名，在API中可能叫userName
    username: str = Field(alias="userName", min_length=3, max_length=20)
    age: Optional[int] = Field(None, ge=0, le=150, description="用户的年龄")
    is_active: bool = True

# 1. 生成默认的（用于验证的）JSON Schema
validation_schema = User.model_json_schema()
print(json.dumps(validation_schema, indent=2, ensure_ascii=False))
# 输出会包含所有验证规则，属性名使用别名“userName”

# 2. 生成用于序列化的JSON Schema
serialization_schema = User.model_json_schema(mode="serialization")
# 注意观察 `is_active` 字段，由于它有默认值，在序列化模式下 `required` 字段列表里可能没有它

# 3. 使用原始字段名生成Schema
schema_by_original_name = User.model_json_schema(by_alias=False)
# 此时属性名是 `username` 而不是 `userName`
