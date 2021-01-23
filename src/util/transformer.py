from datetime import datetime


def transform_but000(table_rows: list) -> dict:

    target = {'but000->type->1': 0, 'but000->type->2': 0, 'but000->type->3': 0,

              'but000->bpkind->p01': 0, 'but000->bpkind->p02': 0, 'but000->pbkind->pj': 0,
              'but000->bpkind->pn': 0, 'but000->bpkind->s4im': 0,

              'but000->bu_group->': 0
              }

    if len(table_rows) == 0:
        return target

    row = max(table_rows, key=lambda r: datetime.strptime(r.find('crdat').text, '%Y-%m-%d'))
    target['but000->type->' + str(row.find('type').text).lower()] = 1
    target['but000->type->' + str(row.find('bpkind').text).lower()] = 1

    print(row.find('bu_group').text)

    return target


def transform_zdkk_rb_scores(table_rows: list):
    pass


def transform_dfkkko(table_rows: list):
    target = {'dfkkko->blart->1': 0}

    if len(table_rows) == 0:
        return target

    return target


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
