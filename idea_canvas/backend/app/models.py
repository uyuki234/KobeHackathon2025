# app/models.py
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, field_validator

class UINode(BaseModel):
    id: str
    roleKey: str
    roleLabel: str
    element: str
    x: float
    y: float
    color: str
    emoji: Optional[str] = None

class UIEdge(BaseModel):
    id: str
    sourceId: str
    targetId: str

class Options(BaseModel):
    tone: Literal["Practical","Creative"] = "Practical"
    count: Literal[3,4,5] = 3


class GenerateReq(BaseModel):
    nodes: List[UINode] = Field(default_factory=list)
    edges: List[UIEdge] = Field(default_factory=list)
    options: Options

    @field_validator("edges")
    @classmethod
    def validate_edges(cls, edges):
        if len(edges) == 0:
            raise ValueError("少なくとも1つの接続が必要です。")
        return edges

class Idea(BaseModel):
    title: str
    desc: str

class GenerateRes(BaseModel):
    ideas: List[Idea]
    usage: Optional[Dict] = None