from django.db.models import *
from django.contrib.auth.models import User
from rest_framework.fields import ListField


# from django.utils import timezone


# Create your models here.
class Type(Model):
    id = AutoField(primary_key=True)
    type_name = TextField('Type', null=False, unique=True)
    type_description = TextField('Type description', null=False, unique=True)
    type_short = TextField('Type short', null=False, unique=True)

    class Meta:
        db_table = 'type'

    def __str__(self):
        return str({'type': self.type_name, 'description': self.type_short})


class InciType(Model):
    CONCENTRATION = [("High", "High"),
                   ("Medium", "Medium"),
                   ("Low", "Low")]
    id = AutoField(primary_key=True)
    inci_id = ForeignKey('Inci', verbose_name='Inci', null=False, on_delete=CASCADE)
    type_id = ForeignKey('Type', verbose_name='Type', null=False, on_delete=CASCADE)
    conc = CharField('Concentration', choices=CONCENTRATION, null=True, default=CONCENTRATION[0])

    class Meta:
        db_table = 'inci_type'

    def __str__(self):
        return str({'INCI_id': self.inci_id, 'Type_id': self.type_id})


class Inci(Model):
    id = AutoField(primary_key=True)
    inci_name = TextField('INCI', null=False, unique=True)
    description = TextField('Description', null=True, unique=True)
    source = TextField('Source', null=True)
    vegan = BooleanField('Vegan', null=True)

    class Meta:
        db_table = 'inci'

    def __str__(self):
        return str({'INCI name': self.inci_name})

class Active(Model):
    id = AutoField(primary_key=True)
    inci_id = ForeignKey('INCI', verbose_name='INCI', null=False, on_delete=CASCADE)
    low_conc = FloatField('Low concentration', null=True, unique=False)
    medium_conc = FloatField('Medium concentration', null=True, unique=False)
    high_conc = FloatField('High concentration', null=True, unique=False)

    class Meta:
        db_table = 'active'

    def __str__(self):
        return str({'inci': self.inci_id,
                    'low': self.low_conc,
                    'medium': self.medium_conc,
                    'high': self.high_conc})

class Ingredient(Model):
    id = AutoField(primary_key=True)
    inci_id = ForeignKey('Inci', verbose_name='INCI', null=False, on_delete=CASCADE, unique=False)
    ingredient = TextField('Ingredient', null=False, unique=True)

    class Meta:
        db_table = 'ingredient'

    def __str__(self):
        return str({'Ingredient': self.ingredient})


class Feature(Model):
    id = AutoField(primary_key=True)
    effect = TextField('Effect', null=False, unique=True)
    benefit = BooleanField('Benefit', null=False)

    class Meta:
        db_table = 'feature'

    def __str__(self):
        return str({'Effect': self.effect})


class InciFeature(Model):
    id = AutoField(primary_key=True)
    inci_id = ForeignKey('Inci', verbose_name='Inci', null=False, on_delete=CASCADE)
    feature_id = ForeignKey('Feature', verbose_name='Feature', null=False, on_delete=CASCADE)

    class Meta:
        db_table = 'inci_feature'

    def __str__(self):
        return str({'INCI_id': self.inci_id, 'Feature_id': self.feature_id})


class Recommendation(Model):
    id = AutoField(primary_key=True)
    recom = TextField('Recommendation', null=False, unique=True)

    class Meta:
        db_table = 'recom'

    def __str__(self):
        return str({'Recommendation': self.recom})


class InciRecom(Model):
    id = AutoField(primary_key=True)
    inci_id = ForeignKey('Inci', verbose_name='Inci', null=False, on_delete=CASCADE)
    recom_id = ForeignKey('Recommendation', verbose_name='Recommendation', null=False, on_delete=CASCADE)

    class Meta:
        db_table = 'inci_recom'

    def __str__(self):
        return str({'INCI_id': self.inci_id, 'Feature_id': self.recom_id})


class Combination(Model):
    COMBINATION = [("Yes", "Yes"),
                   ("Carefully", "Carefully"),
                   ("No", "No")]
    id = AutoField(primary_key=True)
    inci_id_1 = ForeignKey('Inci', verbose_name='Inci 1', related_name='inci_1', null=False, on_delete=CASCADE)
    inci_id_2 = ForeignKey('Inci', verbose_name='Inci 2', related_name='inci_2', null=False, on_delete=CASCADE)
    comb_type = CharField(max_length=10, null=False)
    combination = TextField('Combination', null=False, unique=True)

    class Meta:
        db_table = 'combination'

    def __str__(self):
        return str({'inci 1': self.inci_id_1,
                    'inci 2': self.inci_id_2,
                    'combination type': self.comb_type})


class Record(Model):
    id = AutoField(primary_key=True)
    user_id = ForeignKey(User, verbose_name='User id', null=False, on_delete=CASCADE)
    ingr_list = TextField('Ingredient list', null=False, unique=False)
    conc_list = TextField('Concentration list', null=True, unique=False)
    brand_name = TextField('Brand', null=True)
    product_name = TextField('Product', null=True)
    favorite = BooleanField('Favorite', null=False, default=False)
    datetime = DateTimeField('Datetime', null=False)

    class Meta:
        db_table = 'records'

    def __str__(self):
        return str({'user id': self.user_id,
                    'ingredient list': self.ingr_list,
                    'concentration list': self.conc_list})

class TempRecord(Model):
    id = AutoField(primary_key=True)
    ingr_list = TextField('Ingredient list', null=False, unique=False)
    conc_list = TextField('Concentration list', null=True, unique=False)

    class Meta:
        db_table = 'temp_records'

    def __str__(self):
        return str({'ingredient list': self.ingr_list,
                    'concentration list': self.conc_list})
