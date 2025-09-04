# app/routers/ideas.py (초간단 프로토타입 버전 예시)
from fastapi import APIRouter, HTTPException
from ..models import GenerateReq, GenerateRes, Idea

router = APIRouter(prefix="/api/ideas", tags=["ideas"])

@router.post("/generate", response_model=GenerateRes)
def generate_ideas(body: GenerateReq):
    node_map = {n.id: n for n in body.nodes}
    if not node_map:
        raise HTTPException(status_code=400, detail="no nodes")

    pairs = []
    for e in body.edges:
        if e.sourceId == e.targetId:
            raise HTTPException(status_code=400, detail="self edge")
        if e.sourceId not in node_map or e.targetId not in node_map:
            raise HTTPException(status_code=400, detail="unknown node in edge")
        pairs.append((node_map[e.sourceId], node_map[e.targetId]))

    if not pairs:
        raise HTTPException(status_code=422, detail="no valid pairs")

    # 아주 단순한 결과 생성(톤 분기/장식 제거)
    out = []
    count = body.options.count
    for i in range(count):
        a, b = pairs[i % len(pairs)]
        out.append(Idea(
            title=f"{a.element} x {b.element}",
            desc=f"{a.roleLabel} と {b.roleLabel} の視点を合わせた案"
        ))
    return GenerateRes(ideas=out)