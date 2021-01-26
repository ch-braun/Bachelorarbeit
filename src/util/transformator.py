from datetime import datetime

EXTRACT_DATE = '2020-12-16'
FPZ_TAGS = ['min', 'lq', 'md', 'uq', 'max']


def get_day_diff(date1: str, date2: str) -> int:
    if date1 in ['0000-00-00', '9999-99-99', ''] or date2 in ['0000-00-00', '9999-99-99', '']:
        return 0

    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    delta = date1 - date2
    return abs(delta.days)


def transform_but000(table_rows: list) -> dict:
    target = {'but000->type->1': 0, 'but000->type->2': 0,

              'but000->bpkind->p01': 0, 'but000->bpkind->p02': 0, 'but000->pbkind->pj': 0,
              'but000->bpkind->pn': 0, 'but000->bpkind->s4im': 0,

              'but000->title->0001': 0, 'but000->title->0002': 0, 'but000->title->0003': 0,
              'but000->title->0004': 0, 'but000->title->0005': 0, 'but000->title->0006': 0,
              'but000->title->0007': 0, 'but000->title->0008': 0, 'but000->title->0009': 0,

              'but000->xsexf': 0,
              'but000->xsexm': 0,
              'but000->xsexu': 0,

              'but000->birthdt': 0,
              'but000->natpers': 0,

              'but000->crdat': 0,
              'but000->xdele': 0,

              'but000->title_aca1->0001': 0, 'but000->title_aca1->0002': 0,

              'but000->jobgr->privat': 0, 'but000->jobgr->unternehmen': 0,

              'but000->zzgpsofa': 0, 'but000->zztkke': 0
              }

    if len(table_rows) == 0:
        return target

    row = max(table_rows, key=lambda r: datetime.strptime(r.find('crdat').text, '%Y-%m-%d'))

    target['but000->type->' + str(row.find('type').text).lower()] = 1
    target['but000->bpkind->' + str(row.find('bpkind').text).lower()] = 1

    target['but000->title->' + str(row.find('title').text).lower()] = 1

    target['but000->xsexf'] = 1 if row.find('xsexf').text is not None else 0
    target['but000->xsexm'] = 1 if row.find('xsexm').text is not None else 0
    target['but000->xsexu'] = 1 if row.find('xsexu').text is not None else 0

    target['but000->birthdt'] = get_day_diff(row.find('birthdt').text, EXTRACT_DATE)
    target['but000->natpers'] = 1 if row.find('natpers').text == 'X' else 0

    target['but000->crdat'] = get_day_diff(row.find('crdat').text, EXTRACT_DATE)

    target['but000->xdele'] = 1 if row.find('xdele').text is not None else 0

    if row.find('title_aca1').text is not None:
        target['but000->title_aca1->' + str(row.find('title_aca1').text)] = 1

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


def transform_fkkvkp(table_rows: list):
    target = {'fkkvkp->ezawe->selbst': 0, 'fkkvkp->ezawe->d': 0, 'fkkvkp->ezawe->3': 0, 'fkkvkp->ezawe->4': 0,
              'fkkvkp->ezawe->5': 0, 'fkkvkp->ezawe->e': 0,

              'fkkvkp->zztgr->1': 0, 'fkkvkp->zztgr->30': 0, 'fkkvkp->zztgr->40': 0,
              'fkkvkp->zztgr->0': 0, 'fkkvkp->zztgr->7': 0,

              'fkkvkp->zzcontaendat': 0,
              'fkkvkp->zzloevmaendat': 0,
              'fkkvkp->zzinkstaaendat': 0,

              'fkkvkp->loevm': 0,
              'fkkvkp->zzumst': 0,
              'fkkvkp->zzvp2nato': 0,

              'fkkvkp->zzinkstatus->1': 0, 'fkkvkp->zzinkstatus->2': 0,
              'fkkvkp->zzinkstatus->3': 0, 'fkkvkp->zzinkstatus->4': 0,

              'fkkvkp->zzcontstatus': 0,
              'fkkvkp->abwre': 0
              }

    if len(table_rows) == 0:
        return target

    row = max(table_rows, key=lambda r: datetime.strptime(r.find('erdat').text, '%Y-%m-%d'))
    if row.find('ezawe').text is not None:
        target['fkkvkp->ezawe->' + str(row.find('ezawe').text).lower()] = 1
    else:
        target['fkkvkp->ezawe->selbst'] = 1

    if row.find('zztgr').text is not None:
        target['fkkvkp->zztgr->' + str(int(row.find('zztgr').text)).lower()] = 1

    target['fkkvkp->zzcontaendat'] = get_day_diff(row.find('zzcontaendat').text, EXTRACT_DATE)
    target['fkkvkp->zzloevmaendat'] = get_day_diff(row.find('zzloevmaendat').text, EXTRACT_DATE)
    target['fkkvkp->zzinkstaaendat'] = get_day_diff(row.find('zzinkstaaendat').text, EXTRACT_DATE)

    target['fkkvkp->loevm'] = 1 if str(row.find('loevm').text) == 'X' else 0
    target['fkkvkp->zzumst'] = 1 if str(row.find('zzumst').text) == '1' else 0
    target['fkkvkp->zzvp2nato'] = 1 if row.find('zzvp2nato').text is not None else 0

    if row.find('zzinkstatus').text is not None:
        target['fkkvkp->zzinkstatus->' + str(row.find('zzinkstatus').text).lower()] = 1

    target['fkkvkp->zzcontstatus'] = 1 if row.find('zzcontstatus').text is not None else 0
    target['fkkvkp->abwre'] = 1 if row.find('abwre').text is not None else 0

    return target


def transform_dfkkko(table_rows: list):
    target = {'dfkkko->anzahl_storno': 0}

    blart = ['tr', 'zs', 'tg', 'ze', 'mk', 'gk', 'zm', 'gt', 'as', 'ik', 're', 'rh', 'ed', 'u1', 't2', 't1', 'sk', 'rp',
             'gu', 'gr', 'tz', 'tb', 'zu', 'aa', 'am', 'u3', 'zn', 'ga', 'xa', 'ts', 'ac', 'ag', 'af', 'an', 'u4', 'ec',
             'ti', 'gs', 'd3', 'ms', 'em', 'ao', 'mr', 'rm', 'rd', 'rc', 'ea']
    abgrd = ['leer', 'ai', '1', 'ba', 'am', 'be', 'vj', 'if', '6', 'ac', 'mb', 'as', 'in', 'an', 'rl', 'wf']
    aginf = ['leer', 'ausgleich']
    columns = ['bldat', 'anzahl']

    for art in blart:
        for grd in abgrd:
            for inf in aginf:
                for c in columns:
                    target["dfkkko->" + art + "->" + grd + "->" + inf + "->" + c] = 0

    if len(table_rows) == 0:
        return target

    for row in table_rows:
        art = row.find('blart').text
        stbel = row.find('stbel').text
        if art is not None and stbel is None:
            art = art.lower()
            grd = str(row.find('abgrd').text).lower() if row.find('abgrd').text is not None else 'leer'
            inf = 'ausgleich' if row.find('aginf') else 'leer'
            date = get_day_diff(row.find('bldat').text, EXTRACT_DATE)

            if int(target["dfkkko->" + art + "->" + grd + "->" + inf + "->bldat"]) > 0:
                date = min(date, int(target["dfkkko->" + art + "->" + grd + "->" + inf + "->bldat"]))
            else:
                target["dfkkko->" + art + "->" + grd + "->" + inf + "->bldat"] = date

            target["dfkkko->" + art + "->" + grd + "->" + inf + "->anzahl"] += 1

        elif stbel is not None:
            target['dfkkko->anzahl_storno'] += 1

    return target


def transform_dfkkop(table_rows: list):
    target = dict()

    blart = ['tr', 'tg', 'mk', 'ik', 're', 'rh', 'ze', 'zm', 'gk', 'ed', 'u1', 't2', 't1', 'sk', 'rp', 'gu', 'gr', 'as',
             'tz', 'tb', 'am', 'ga', 'xa', 'ts', 'aa', 'ac', 'ag', 'u3', 'gt', 'zn', 'an', 'u4', 'zu', 'gs', 'af', 'ms',
             'mr', 'zs', 'rm', 'rd', 'rc', 'ec', 'd3', 'ea']
    zzrlanz = ['kein_rueckl', 'rueckl']
    augst = ['offen', 'ausgl']
    columns = ['augdt', 'betrh', 'whang']
    
    for art in blart:
        for rueckl in zzrlanz:
            for ausgl in augst:
                for c in columns:
                    target['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->' + c] = 0

    if len(table_rows) == 0:
        return target
    temp = dict()
    for row in table_rows:
        art = row.find('blart').text
        if art is not None:
            art = art.lower()
            rueckl = 'rueckl' if int(row.find('zzrlanz').text) > 0 else 'kein_rueckl'
            ausgl = 'ausgl' if row.find('augst').text is not None else 'offen'
            betrh = float(row.find('betrh').text)
            whang = int(row.find('whang').text)
            if row.find('augdt') is not None and row.find('faedn') is not None:
                augdt = get_day_diff(row.find('augdt').text, row.find('faedn').text)
            else:
                augdt = 0

            if 'dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->betrh' not in temp.keys():
                temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->betrh'] = []
            temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->betrh'].append(betrh)

            if 'dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->whang' not in temp.keys():
                temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->whang'] = []
            temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->whang'].append(whang)

            if 'dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->augdt' not in temp.keys():
                temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->augdt'] = []
            if augdt != 0:
                temp['dfkkop->' + art + '->' + rueckl + '->' + ausgl + '->augdt'].append(augdt)

    for key in temp.keys():
        if key.endswith('betrh'):
            target[key] = round(sum(temp[key]), 2)
        elif (key.endswith('whang') or key.endswith('augdt')) and len(temp[key]) > 0:
            target[key] = round(float(sum(temp[key]) / len(temp[key])), 2)

    for key in target:
        if target[key] > 0:
            print(key, ':', target[key])

    return target


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
