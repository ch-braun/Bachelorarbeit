from transformer_table import *


class Transformer:

    __map_table_transformer = {
        'but000': TransformerBut000,
        'zdkk_rb_scores': TransformerZdkk_rb_scores,
        'dfkkko': TransformerDfkkko,
        'dfkkop': TransformerDfkkop,
        'but0bk': TransformerBut0bk,
        'fkkmaze': TransformerFkkmaze,
        'fkkmako': TransformerFkkmako,
        'dfkklocks': TransformerDfkklocks,
        'zdkk_mw_vtref_st': TransformerZdkk_mw_vtref_st,
        'dfkkzk': TransformerDfkkzk,
        'dpayh': TransformerDpayh,
        'fkk_instpln_head': TransformerFkk_instpln_head,
        'dfkkrk': TransformerDfkkrk,
        'zdkk_bapi_obcfc': TransformerZdkk_bapi_obcfc,
        'zdkk_bapi_obbel': TransformerZdkk_bapi_obbel,
        'zdkk_zv_azahl': TransformerZdkk_zv_azahl,
        'zdkk_crpo': TransformerZdkk_crpo,
        'zdkk_dk_san_bas': TransformerZdkk_dk_san_bas,
        'zdkk_abg_n_cfc': TransformerZdkk_abg_n_cfc,
        'fkk_sec': TransformerFkk_sec,
        'fkk_sec_c': TransformerFkk_sec_c
        }

    def __init__(self, table_rows: list):
        self.table_rows = table_rows
        self.transformed_row = dict()

    def transform(self) -> dict:
        return self.transformed_row

    def get_transformer_for_table_rows(self, table_name: str, table_rows: list):
        return self.__map_class_to_table(table_name)(table_rows)

    def __map_class_to_table(self, table: str):
        if table in self.__map_table_transformer.keys():
            return self.__map_table_transformer[table]
        else:
            return Transformer
