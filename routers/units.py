from fastapi import APIRouter, Query, Header, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import apaginate
from schemas import UnitItem
from services import build_unit_query
from models import UnitModel

router = APIRouter(prefix="/units", tags=["units"])


@router.get("/{unit_id}", response_model=UnitItem)
async def get_unit(unit_id: int) -> UnitItem:
    """Возвращает один юнит по его идентификатору."""
    unit = await UnitModel.get_or_none(unit_id=unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="Юнит не найден")
    return UnitItem.model_validate(unit)


@router.get("", response_model=Page[UnitItem])
async def get_units(
    era_id: int | None = None,
    faction_id: list[int] | None = Query(None),
    unit_type: str | None = None,
    title: str | None = None,
    role: str | None = None,
    specials: str | None = Query(None, min_length=2),
    pv: int | None = None,
    sz: int | None = None,
    short: int | None = None,
    medium: int | None = None,
    long: int | None = None,
    extreme: int | None = None,
    ov: int | None = None,
    armor: int | None = None,
    struc: int | None = None,
    threshold: int | None = None,
    mv: int | None = None,
    sort_by: str | None = Query(None),
    sort_order: str = Query("asc"),

    x_specials_mode: str = Header("or", alias="X-Specials-Mode"),
    x_pv_mode: str = Header("eq", alias="X-Pv-Mode"),
    x_sz_mode: str = Header("eq", alias="X-Sz-Mode"),
    x_short_mode: str = Header("eq", alias="X-Short-Mode"),
    x_medium_mode: str = Header("eq", alias="X-Medium-Mode"),
    x_long_mode: str = Header("eq", alias="X-Long-Mode"),
    x_extreme_mode: str = Header("eq", alias="X-Extreme-Mode"),
    x_ov_mode: str = Header("eq", alias="X-Ov-Mode"),
    x_armor_mode: str = Header("eq", alias="X-Armor-Mode"),
    x_struc_mode: str = Header("eq", alias="X-Struc-Mode"),
    x_threshold_mode: str = Header("eq", alias="X-Threshold-Mode"),
    x_mv_mode: str = Header("eq", alias="X-Mv-Mode"),
) -> Page[UnitItem]:
    valid_modes = {"eq", "gt", "gte", "lt", "lte"}
    mode_headers = {
        "x_pv_mode": x_pv_mode,
        "x_sz_mode": x_sz_mode,
        "x_short_mode": x_short_mode,
        "x_medium_mode": x_medium_mode,
        "x_long_mode": x_long_mode,
        "x_extreme_mode": x_extreme_mode,
        "x_ov_mode": x_ov_mode,
        "x_armor_mode": x_armor_mode,
        "x_struc_mode": x_struc_mode,
        "x_threshold_mode": x_threshold_mode,
        "x_mv_mode": x_mv_mode,
    }
    for header_name, mode_value in mode_headers.items():
        if mode_value not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Невалидное значение заголовка {header_name}: '{mode_value}'."
                       f"Допустимые значения: {', '.join(valid_modes)}"
            )

    if sort_order.lower() not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail=f"Невалидное значение sort_order: '{sort_order}'. "
                   f"Допустимые значения: asc, desc"
        )

    query = await build_unit_query(
        era_id=era_id,
        faction_id=faction_id,
        unit_type=unit_type,
        title=title,
        role=role,
        specials=specials,
        x_specials_mode=x_specials_mode,
        pv=pv,
        sz=sz,
        short=short,
        medium=medium,
        long=long,
        extreme=extreme,
        ov=ov,
        armor=armor,
        struc=struc,
        threshold=threshold,
        mv=mv,
        x_pv_mode=x_pv_mode,
        x_sz_mode=x_sz_mode,
        x_short_mode=x_short_mode,
        x_medium_mode=x_medium_mode,
        x_long_mode=x_long_mode,
        x_extreme_mode=x_extreme_mode,
        x_ov_mode=x_ov_mode,
        x_armor_mode=x_armor_mode,
        x_struc_mode=x_struc_mode,
        x_threshold_mode=x_threshold_mode,
        x_mv_mode=x_mv_mode,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return await apaginate(query.distinct())
