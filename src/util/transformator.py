from datetime import datetime

EXTRACT_DATE = '2020-12-16'


def get_day_diff(date1: str, date2: str) -> int:
    if date1 in ['0000-00-00', '9999-99-99', ''] or date2 in ['0000-00-00', '9999-99-99', '']:
        return 0

    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    delta = date1 - date2
    return abs(delta.days)


def transform_but000(table_rows: list) -> dict:
    target = {'but000->type->1': 0, 'but000->type->2': 0, 'but000->type->3': 0,

              'but000->bpkind->p01': 0, 'but000->bpkind->p02': 0, 'but000->pbkind->pj': 0,
              'but000->bpkind->pn': 0, 'but000->bpkind->s4im': 0,

              'but000->title->0001': 0, 'but000->title->0002': 0, 'but000->title->0003': 0,
              'but000->title->0004': 0, 'but000->title->0005': 0, 'but000->title->0006': 0,
              'but000->title->0007': 0, 'but000->title->0008': 0, 'but000->title->0009': 0,

              'but000->found_dat': 0,
              'but000->liquid_dat': 0,

              'but000->xsexf': 0,
              'but000->xsexm': 0,
              'but000->xsexu': 0,

              'but000->birthdt': 0,
              'but000->deathdt': 0,

              'but000->perno': 0,
              'but000->crdat': 0,
              'but000->xdele': 0,

              'but000->title_aca1->0001': 0, 'but000->title_aca1->0002': 0, 'but000->title_aca1->0003': 0,
              'but000->title_aca1->0004': 0, 'but000->title_aca1->0005': 0, 'but000->title_aca1->0006': 0,
              'but000->title_aca1->ding': 0, 'but000->title_aca1->dr': 0, 'but000->title_aca1->magi': 0,

              'but000->jobgr->privat': 0, 'but000->jobgr->unternehmen': 0,

              'but000->zzgpsofa': 0, 'but000->zztkke': 0
              }

    if len(table_rows) == 0:
        return target

    row = max(table_rows, key=lambda r: datetime.strptime(r.find('crdat').text, '%Y-%m-%d'))

    target['but000->type->' + str(row.find('type').text).lower()] = 1
    target['but000->bpkind->' + str(row.find('bpkind').text).lower()] = 1

    target['but000->title->' + str(row.find('title').text).lower()] = 1

    target['but000->found_dat'] = get_day_diff(row.find('found_dat').text, EXTRACT_DATE)
    target['but000->liquid_dat'] = get_day_diff(row.find('liquid_dat').text, EXTRACT_DATE)

    target['but000->xsexf'] = 1 if row.find('xsexf').text is not None else 0
    target['but000->xsexm'] = 1 if row.find('xsexm').text is not None else 0
    target['but000->xsexu'] = 1 if row.find('xsexu').text is not None else 0

    target['but000->birthdt'] = get_day_diff(row.find('birthdt').text, EXTRACT_DATE)
    target['but000->deathdt'] = get_day_diff(row.find('deathdt').text, EXTRACT_DATE)

    target['but000->perno'] = 1 if (int(row.find('perno').text) + int(row.find('zzperno').text)) > 0 else 0

    target['but000->crdat'] = get_day_diff(row.find('crdat').text, EXTRACT_DATE)

    target['but000->xdele'] = 1 if row.find('xdele').text is not None else 0

    if row.find('title_aca1').text is not None:
        target['but000->title_aca1->' + str(row.find('title_aca1').text).lower()] = 1

    if row.find('jobgr').text is not None:
        job_int = int(row.find('jobgr').text)
        if job_int < 10:
            target['but000->jobgr->privat'] = 1
        else:
            target['but000->jobgr->unternehmen'] = 1

    if row.find('zzgpsofa').text is not None:
        target['but000->zzgpsofa'] = int(row.find('zzgpsofa').text)

    if row.find('zztkke').text is not None:
        target['but000->zztkke'] = int(row.find('zztkke').text)

    return target


def transform_zdkk_rb_scores(table_rows: list):
    # Bildet Klassifikation, nicht Datenbasis
    pass


def transform_dfkkko(table_rows: list):
    # TODO
    target = {'dfkkko->blart->aa': 0}

    if len(table_rows) == 0:
        return target

    return target


def transform_dfkkop(table_rows: list):
    pass


def transform_but0bk(table_rows: list):
    target = {
        'but0bk->xezer': 0, 'but0bk->moves': 0
    }

    if len(table_rows) == 0:
        return target

    for row in table_rows:
        if row.find('xezer').text is not None:
            target['but0bk->xezer'] = 1
            break

    target['but0bk->moves'] = len(table_rows) - 1

    return target


def transform_fkkmaze(table_rows: list):
    # TODO
    target = {
        'fkkmaze->01->mazae': 0, 'fkkmaze->01->': 0
    }

    if len(table_rows) == 0:
        return target


def transform_fkkmako(table_rows: list):
    # TODO
    pass


def transform_dfkklocks(table_rows: list):
    target = {
        'fkkmaze->01->mazae': 0, 'fkkmaze->01->': 0
    }

    if len(table_rows) == 0:
        return target


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
