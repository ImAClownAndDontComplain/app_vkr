from typing import Optional, Iterable, List
from datetime import datetime
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import *

RECORD = ['aqua', 'caprylic/capric triglyceride',
 'cetearyl glucoside', 'peg-100 stearate',
 '1,2-hexanediol', 'propylene glycol', 'phenoxyethanol',
 'candida bombicola/glucose/methyl rapeseedate ferment',
 'пэг-40 гидрогенизированное касторовое масло', 'метилизотиазолинон']

RECORD_STR = 'aqua,caprylic/capric triglyceride,cetearyl glucoside,peg-100 stearate,1,2-hexanediol,propylene glycol,phenoxyethanol,candida bombicola/glucose/methyl rapeseedate ferment,пэг-40 гидрогенизированное касторовое масло,метилизотиазолинон'

# inci_get
def get_inci_by_id(id: int) -> Optional[Inci]:
    return Inci.objects.filter(id=id).first()

def get_inci_by_name(name: str) -> Optional[Inci]:
    return Inci.objects.filter(inci_name=name).first()

def get_all_inci() -> Inci:
    return Inci.objects.all()

def add_description(id: int) -> None:
    inci = get_inci_by_id(id)
    if inci is not None:
        types = Inci.objects.filter(inci=inci)
    return Inci.objects.all()


# actives
def check_if_active_by_id(id: int) -> bool:
    types = get_types_by_inci_id(id)
    for type in types:
        if type.type_name == 'active':
            return True
    return False


def check_if_active_by_inci(inci: Inci) -> bool:
    types = get_types_by_inci(inci)
    for type_inci in types:
        if type_inci.type_name == 'active':
            return True
    return False

def check_if_active_by_name(name: str) -> bool:
    types = get_types_by_inci_name(name)
    for type in types:
        if type.type_name == 'active':
            return True
    return False

def get_conc_by_id(id: int) -> [float, float, float]:
    if check_if_active_by_id(id) is True:
        inci = get_inci_by_id(id)
        active = Active.objects.filter(inci_id=inci).first()
        return [active.low_conc, active.medium_conc, active.high_conc]

def get_conc_by_inci(inci: Inci) -> [float, float, float]:
    if check_if_active_by_inci(inci) is True:
        active = Active.objects.filter(inci_id=inci).first()
        return [active.low_conc, active.medium_conc, active.high_conc]


# def get_conc_by_name(name: str) -> [float, float, float]:
#     if check_if_active_by_name(name) is True:
#         inci = get_inci_by_name(name)
#         active = Active.objects.filter(inci_id=inci).first()
#         return [active.low_conc, active.medium_conc, active.high_conc]

# ingr_get
def get_ingredient_by_id(id: int) -> Optional[Ingredient]:
    return Ingredient.objects.filter(id=id).first()

def get_ingredient_by_name(name: str) -> Optional[Ingredient]:
    return Ingredient.objects.filter(ingr_name=name).first()

def get_all_ingredients() -> Ingredient:
    return Ingredient.objects.all()

def get_all_ingredients_by_inci_id(id: int) -> Ingredient:
    return Ingredient.objects.filter(inci_id=id).all()

def get_all_ingredients_by_inci_name(name: str) -> Ingredient:
    inci = get_inci_by_name(name)
    return Ingredient.objects.filter(inci_id=inci.id).all()

# types
def get_type_by_id(id: int) -> Optional[Type]:
    return Type.objects.filter(id=id).first()

def get_type_by_name(name: str) -> Optional[Type]:
    return Type.objects.filter(type_name=name).first()

def get_types_by_inci(inci: Inci) -> List[Type]:
    incis = InciType.objects.filter(inci_id=inci).all()
    res = []
    for inci in incis:
        type_inci = inci.type_id
        res.append(type_inci)
    return res

def get_types_by_inci_id(id: int) -> List[Type]:
    inci_id = get_inci_by_id(id)
    incis = InciType.objects.filter(inci_id=inci_id).all()
    res = []
    for inci in incis:
        type = inci.type_id
        res.append(type)
    return res

def get_types_by_inci_name(name: str) -> List[Type]:
    inci_name = get_inci_by_name(name)
    incis = InciType.objects.filter(inci_id=inci_name).all()
    res = []
    for inci in incis:
        type = inci.type_id
        res.append(type)
    return res


# inci_by_ingr
def get_inci_by_ingredient_id(id: int) -> Optional[Inci]:
    inci_id = get_ingredient_by_id(id).inci_id
    return get_inci_by_id(inci_id.id)

def get_inci_by_ingredient_name(name: str) -> Optional[Inci]:
    inci_id = get_ingredient_by_name(name).inci_id
    return get_inci_by_id(inci_id.id)


# combo
def get_comb_by_inci_ids(id1: int, id2: int) -> Optional[Combination]:
    inci_id_1 = get_inci_by_id(id1)
    inci_id_2 = get_inci_by_id(id2)
    return Combination.objects.filter(inci_id1=inci_id_1, inci_id2=inci_id_2).first()

def get_comb_by_inci_names(name1: str, name2: str) -> Optional[Combination]:
    inci_id_1 = get_inci_by_name(name1)
    inci_id_2 = get_inci_by_name(name2)
    return Combination.objects.filter(inci_id1=inci_id_1, inci_id2=inci_id_2).first()

def get_all_combs_by_inci_id(id: int) -> Combination:
    inci = get_inci_by_id(id)
    return Combination.objects.filter(inci_id_1=inci)

def get_all_combs_by_inci_name(name: str) -> Combination:
    inci = get_inci_by_name(name)
    return Combination.objects.filter(inci_id_1=inci)


# features
def get_feature_by_id(id: int) -> Optional[Feature]:
    return Feature.objects.filter(id=id)

def get_all_features() -> Feature:
    return Feature.objects.all()

def get_features_by_inci_id(id: int) -> Feature:
    inci = get_inci_by_id(id)
    return Feature.objects.filter(inci_id=inci.id).all()

def get_features_by_inci(inci: Inci) -> List[Feature]:
    inci_feature = InciFeature.objects.filter(inci_id=inci).all()
    features = []
    for feature in inci_feature:
        features.append(get_feature_by_id(feature.feature_id))
    return features

def get_features_by_inci_name(name: str) -> Feature:
    inci = get_inci_by_name(name)
    return Feature.objects.filter(inci_id=inci).all()

def get_incis_by_feature_id(id: int) -> List[Inci]:
    feature_id = get_feature_by_id(id)
    if feature_id is not None:
        features = InciFeature.objects.filter(feature_id=feature_id).all()
        incis = []
        for feature in features:
            inci = get_inci_by_id(feature.inci_id)
            incis.append(inci)
        return incis



# recom
def get_recom_by_id(id: int) -> Optional[Recommendation]:
    return Recommendation.objects.filter(id=id).first()

def get_all_recoms() -> Recommendation:
    return Recommendation.objects.all()

def get_all_recoms_by_inci_id(id: int) -> Recommendation:
    inci = get_inci_by_id(id)
    return InciRecom.objects.filter(inci_id=inci).all()

def get_all_recoms_by_inci_name(name: str) -> Recommendation:
    inci = get_inci_by_name(name)
    return InciRecom.objects.filter(inci_id=inci).all()


# user
def get_user_by_id(id: int) -> Optional[User]:
    return User.objects.get(id=id)


# record
def get_record_by_id(id: int) -> Optional[Record]:
    return Record.objects.filter(id=id).first()

def get_all_records_by_user_id(id: int) -> Record:
    return Record.objects.filter(user_id=id).all()

def get_favorites_by_user_id(id: int) -> Record:
    return Record.objects.filter(user_id=id, favorite=True).all()

def add_record(id: int, ingr_list: str, date_time: datetime) -> None:
    user = get_user_by_id(id)
    record = Record.objects.create(User=user, ingr_list=ingr_list, datetime=date_time)
    record.save()
    return

def add_record_now(id: int, ingr_list: str) -> None:
    user = get_user_by_id(id)
    date_time = datetime.now()
    record = Record.objects.create(user_id=user, ingr_list=ingr_list, datetime=date_time)
    record.save()
    return

def add_record_to_favorites(id: int) -> None:
    record = get_record_by_id(id)
    if record is not None:
        record.favorite = True
        record.save()
    return

def delete_record_from_favorites(id: int) -> None:
    record = get_record_by_id(id)
    if record is not None:
        record.favorite = False
        record.save()
    return

def update_favorite(id: int, brand_name: str, product_name: str) -> None:
    record = get_record_by_id(id)
    if record is not None:
        if record.favorite is True:
            record.brand_name = brand_name
            record.product_name = product_name
            record.save()
    return

def delete_record_by_id(id: int) -> None:
    record = get_record_by_id(id)
    if record is not None:
        record.delete()
    return

def delete_all_records(id: int) -> None:
    user = get_user_by_id(id)
    if user is not None:
        records = Record.objects.filter(user_id=user).all()
        for record in records:
            record.delete()
    return

def delete_all_records_exc_fav(id: int) -> None:
    user = get_user_by_id(id)
    if user is not None:
        records = Record.objects.filter(user_id=user).all()
        for record in records:
            if record.favorite is False:
                record.delete()
    return

def delete_favorites(id: int) -> None:
    user = get_user_by_id(id)
    if user is not None:
        records = Record.objects.filter(user_id=user).all()
        for record in records:
            if record.favorite is True:
                record.delete()
    return







