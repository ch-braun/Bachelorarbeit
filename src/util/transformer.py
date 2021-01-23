def transform_but000(table_rows: list):
    pass


def transform_zdkk_rb_scores(table_rows: list):
    pass


def transform_dfkkko(table_rows: list):
    pass


def transform_dfkkop(table_rows: list):
    pass


def transform_but0bk(table_rows: list):
    pass


def transform_fkkmaze(table_rows: list):
    pass


def transform_fkkmako(table_rows: list):
    pass


def transform_dfkklocks(table_rows: list):
    pass


def transform_zdkk_mw_vtref_st(table_rows: list):
    pass


def transform_dfkkzk(table_rows: list):
    pass


def transform_dpayh(table_rows: list):
    pass


def transform_fkk_instpln_head(table_rows: list):
    pass


def transform_dfkkrk(table_rows: list):
    pass


def transform_zdkk_bapi_obcfc(table_rows: list):
    pass


def transform_zdkk_bapi_obbel(table_rows: list):
    pass


def transform_zdkk_zv_azahl(table_rows: list):
    pass


def transform_zdkk_crpo(table_rows: list):
    pass


def transform_zdkk_dk_san_bas(table_rows: list):
    pass


def transform_zdkk_abg_n_cfc(table_rows: list):
    pass


def transform_fkk_sec(table_rows: list):
    pass


def transform_fkk_sec_c(table_rows: list):
    pass

#
# map_table_transformer = {
#     'but000': transform_but000,
#     'zdkk_rb_scores': transform_zdkk_rb_scores,
#     'dfkkko': transform_dfkkko,
#     'dfkkop': transform_dfkkop,
#     'but0bk': transform_but0bk,
#     'fkkmaze': transform_fkkmaze,
#     'fkkmako': transform_fkkmako,
#     'dfkklocks': transform_dfkklocks,
#     'zdkk_mw_vtref_st': transform_zdkk_mw_vtref_st,
#     'dfkkzk': TransformerDfkkzk,
#     'dpayh': TransformerDpayh,
#     'fkk_instpln_head': TransformerFkk_instpln_head,
#     'dfkkrk': TransformerDfkkrk,
#     'zdkk_bapi_obcfc': TransformerZdkk_bapi_obcfc,
#     'zdkk_bapi_obbel': TransformerZdkk_bapi_obbel,
#     'zdkk_zv_azahl': TransformerZdkk_zv_azahl,
#     'zdkk_crpo': TransformerZdkk_crpo,
#     'zdkk_dk_san_bas': TransformerZdkk_dk_san_bas,
#     'zdkk_abg_n_cfc': TransformerZdkk_abg_n_cfc,
#     'fkk_sec': TransformerFkk_sec,
#     'fkk_sec_c': TransformerFkk_sec_c
# }


def get_transform_func_for_table_rows(table_name: str):
    return map_class_to_table(table_name)


def map_class_to_table(table: str):
    if 'transform_' + table in globals():
        return globals()['transform_' + table]
    else:
        return None


def get_relevant_table_names():
    global_names = filter(lambda name: name.startswith('transform_'), globals().keys())
    global_names = [name.replace('transform_', '') for name in global_names]
    return sorted(global_names)
