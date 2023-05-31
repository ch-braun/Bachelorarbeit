from datetime import datetime
import numpy as np

EXTRACT_DATE = '2020-12-16'
FPZ_TAGS = ['min', 'lq', 'md', 'uq', 'max']


def get_day_diff(date1: str, date2: str) -> int:
    if date1 in ['0000-00-00', '9999-99-99', ''] or date2 in ['0000-00-00', '9999-99-99', '']:
        return 0
    try:
        date1 = datetime.strptime(date1, '%Y-%m-%d')
        date2 = datetime.strptime(date2, '%Y-%m-%d')
        delta = date1 - date2
        return abs(delta.days)
    except ValueError:
        return 0


def transform_but000(table_rows: list) -> dict:
    target = {'but000->type->1': 0, 'but000->type->2': 0,

              'but000->bpkind->p01': 0, 'but000->bpkind->p02': 0, 'but000->bpkind->pj': 0,
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
    if row.find('type').text is not None:
        target['but000->type->' + str(row.find('type').text).lower()] = 1
    if row.find('bpkind').text is not None:
        target['but000->bpkind->' + str(row.find('bpkind').text).lower()] = 1
    if row.find('title').text is not None:
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
    abgrd = ['leer', 'ai', '01', 'ba', 'am', 'be', 'vj', 'if', '06', 'ac', 'mb', 'as', 'in', 'an', 'rl', 'wf']
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
                target["dfkkko->" + art + "->" + grd + "->" + inf + "->bldat"] = \
                    min(date, int(target["dfkkko->" + art + "->" + grd + "->" + inf + "->bldat"]))
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
        posten_ruecknahme = row.find('augob').text
        if art is not None and posten_ruecknahme is None:
            art = art.lower()
            rueckl = 'rueckl' if int(row.find('zzrlanz').text) > 0 else 'kein_rueckl'
            ausgl = 'ausgl' if row.find('augst').text is not None and row.find('xragl').text is None else 'offen'
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


def transform_fkkmako(table_rows: list):
    target = dict()

    zzfokat = ['tk', 'co', 'hw', 'leer']
    columns = ['mazae', 'nexdt', 'zzlastdat', 'msalm->summe', 'msalm->durchschnitt',
               'mahns->max', 'mahns->summe', 'mge1m', 'score']

    for kat in zzfokat:
        for c in columns:
            target['fkkmako->' + kat + '->' + c] = 0

    if len(table_rows) == 0:
        return target

    temp = dict()
    for row in table_rows:
        kat = row.find('zzfokat').text
        storno = row.find('xmsto').text

        if kat is None:
            kat = 'leer'
        else:
            kat = kat.lower()

        if storno != 'X':
            if row.find('mazae') is not None:
                mazae = int(row.find('mazae').text)
                if 'fkkmako->' + kat + '->mazae' not in temp.keys():
                    temp['fkkmako->' + kat + '->mazae'] = []
                temp['fkkmako->' + kat + '->mazae'].append(mazae)

            if row.find('mahns') is not None:
                mahns = int(row.find('mahns').text)
                if 'fkkmako->' + kat + '->mahns' not in temp.keys():
                    temp['fkkmako->' + kat + '->mahns'] = []
                temp['fkkmako->' + kat + '->mahns'].append(mahns)

            if row.find('ausdt') is not None and row.find('nexdt') is not None:
                nexdt = get_day_diff(row.find('ausdt').text, row.find('nexdt').text)
                if nexdt != 0:
                    if 'fkkmako->' + kat + '->nexdt' not in temp.keys():
                        temp['fkkmako->' + kat + '->nexdt'] = []
                    temp['fkkmako->' + kat + '->nexdt'].append(nexdt)

            if row.find('ausdt') is not None and row.find('zzlastdat') is not None:
                lastdat = get_day_diff(row.find('ausdt').text, row.find('zzlastdat').text)
                if lastdat != 0:
                    if 'fkkmako->' + kat + '->zzlastdat' not in temp.keys():
                        temp['fkkmako->' + kat + '->zzlastdat'] = []
                    temp['fkkmako->' + kat + '->zzlastdat'].append(lastdat)

            if row.find('msalm') is not None:
                saldo = float(row.find('msalm').text)
                if 'fkkmako->' + kat + '->msalm' not in temp.keys():
                    temp['fkkmako->' + kat + '->msalm'] = []
                temp['fkkmako->' + kat + '->msalm'].append(saldo)

            if row.find('mge1m') is not None:
                gebuehr = float(row.find('mge1m').text)
                if 'fkkmako->' + kat + '->mge1m' not in temp.keys():
                    temp['fkkmako->' + kat + '->mge1m'] = []
                temp['fkkmako->' + kat + '->mge1m'].append(gebuehr)

            if row.find('score') is not None:
                score = int(row.find('score').text)
                if 'fkkmako->' + kat + '->score' not in temp.keys():
                    temp['fkkmako->' + kat + '->score'] = []
                temp['fkkmako->' + kat + '->score'].append(score)

    for key in temp.keys():
        if key.endswith('mazae'):
            target[key] = max(temp[key])

        elif key.endswith('mahns'):
            target[key + '->summe'] = sum(temp[key])
            target[key + '->max'] = max(temp[key])

        elif key.endswith('nexdt') and len(temp[key]) > 0:
            target[key] = round(float(sum(temp[key]) / len(temp[key])), 2)

        elif key.endswith('zzlastdat') and len(temp[key]) > 0:
            target[key] = round(float(sum(temp[key]) / len(temp[key])), 2)

        elif key.endswith('msalm'):
            target[key + '->summe'] = sum(temp[key])
            if len(temp[key]) > 0:
                target[key + '->durchschnitt'] = round(float(sum(temp[key]) / len(temp[key])), 2)

        elif key.endswith('mge1m') and len(temp[key]) > 0:
            target[key] = round(float(sum(temp[key]) / len(temp[key])), 2)

        elif key.endswith('score') and len(temp[key]) > 0:
            target[key] = round(float(sum(temp[key]) / len(temp[key])), 2)

    return target


def transform_dfkklocks(table_rows: list):
    target = dict()

    lockr = ['ß', 'm', 'l', 'c', 'a', 'h', '3', 'f', 'e', 'b', 'j', 'w', 'k', '5', 'p', 'ä', 'd', 't', '2', 'y', '7',
             'ü', 'v', '1', 'i', 'g', '9', '4', '6', 'o', 'n', 'u', 'r', 'z', 's', 'x', 'q']

    for reason in lockr:
        target['dfkklocks->' + reason + '->anzahl'] = 0

    if len(table_rows) == 0:
        return target

    for row in table_rows:
        reason = row.find('lockr').text
        if reason is not None:
            target['dfkklocks->' + reason.lower() + '->anzahl'] += 1

    return target


def transform_zdkk_mw_vtref_st(table_rows: list):
    target = {'zdkk_mw_vtref_st->zzvtref_status->latest': 0, 'zdkk_mw_vtref_st->zzvtref_status->min': 0,
              'zdkk_mw_vtref_st->zzvtref_status->q1': 0, 'zdkk_mw_vtref_st->zzvtref_status->median': 0,
              'zdkk_mw_vtref_st->zzvtref_status->q3': 0, 'zdkk_mw_vtref_st->zzvtref_status->max': 0,
              'zdkk_mw_vtref_st->zzvtref_status->anzahl': 0}

    if len(table_rows) == 0:
        return target

    latest = None
    latest_date = None
    status = list()
    for row in table_rows:
        row_stat = row.find('zzvtref_status').text
        if row_stat is not None:
            row_stat = int(row_stat)
            status.append(row_stat)
            if latest is None or latest_date < row.find('aedat').text:
                latest = row_stat
                latest_date = row.find('aedat').text

    target['zdkk_mw_vtref_st->zzvtref_status->latest'] = latest
    target['zdkk_mw_vtref_st->zzvtref_status->anzahl'] = len(status)
    if len(status) > 0:
        target['zdkk_mw_vtref_st->zzvtref_status->min'] = min(status)
        target['zdkk_mw_vtref_st->zzvtref_status->q1'] = np.percentile(status, 25)
        target['zdkk_mw_vtref_st->zzvtref_status->median'] = np.percentile(status, 50)
        target['zdkk_mw_vtref_st->zzvtref_status->q3'] = np.percentile(status, 75)
        target['zdkk_mw_vtref_st->zzvtref_status->max'] = max(status)

    return target


def transform_dfkkzk(table_rows: list):
    target = {'dfkkzk->budat->latest': 0,
              'dfkkzk->summs->summe': 0, 'dfkkzk->summs->durchschnitt': 0,
              'dfkkzk->anzahl': 0}

    if len(table_rows) == 0:
        return target

    summe = 0.0
    anzahl = 0
    latest = 0
    for row in table_rows:
        budat = row.find('budat').text
        summs = row.find('summs').text

        if summs is not None:
            summe += float(summs)
            anzahl += 1

        if budat is not None:
            diff = get_day_diff(budat, EXTRACT_DATE)
            if diff != 0 and (latest == 0 or diff < latest):
                latest = diff

    target['dfkkzk->budat->latest'] = latest
    target['dfkkzk->summs->summe'] = round(summe, 2)
    target['dfkkzk->anzahl'] = anzahl
    if anzahl > 0:
        target['dfkkzk->summs->durchschnitt'] = round(float(summe / anzahl), 2)

    return target


def transform_dpayh(table_rows: list):
    target = {'dpayh->valut->latest': 0,
              'dpayh->rbetr->summe': 0, 'dpayh->rbetr->durchschnitt': 0,
              'dpayh->anzahl': 0}

    if len(table_rows) == 0:
        return target

    betraege = list()
    latest = 0
    for row in table_rows:
        valut = row.find('valut').text
        rbetr = row.find('rbetr').text

        if rbetr is not None:
            betraege.append(float(rbetr))

        if valut is not None:
            diff = get_day_diff(valut, EXTRACT_DATE)
            if diff != 0 and (latest == 0 or diff < latest):
                latest = diff

    target['dpayh->valut->latest'] = latest
    target['dpayh->rbetr->summe'] = round(sum(betraege), 2)
    target['dpayh->anzahl'] = len(betraege)
    if len(betraege):
        target['dpayh->rbetr->durchschnitt'] = round(float(sum(betraege) / len(betraege)), 2)

    return target


def transform_fkk_instpln_head(table_rows: list):
    target = dict()

    rpcat = ['sk', 'rp', 'rf']
    deagd = ['leer', '01', '03', '04', '05', '06']

    columns = ['anzahl', 'deadt', 'deoff->durchschnitt', 'deoff->summe', 'deoff->max', 'sttdt', 'ninst']

    for kat in rpcat:
        for grund in deagd:
            for c in columns:
                target['fkk_instpln_head->' + kat + '->' + grund + '->' + c] = 0

    if len(table_rows) == 0:
        return target

    deoff = dict()
    ninst = dict()
    sttdt = dict()
    for row in table_rows:
        kat = row.find('rpcat').text
        deagd = row.find('deagd').text
        if kat is not None:
            kat = kat.lower()
            if deagd is not None:
                deagd = deagd.lower()
            else:
                deagd = 'leer'

            if kat not in deoff.keys():
                deoff[kat] = dict()
            if deagd not in deoff[kat].keys():
                deoff[kat][deagd] = list()
            deoff[kat][deagd].append(float(row.find('deoff').text))

            if kat not in ninst.keys():
                ninst[kat] = dict()
            if deagd not in ninst[kat].keys():
                ninst[kat][deagd] = list()
            ninst[kat][deagd].append(int(row.find('ninst').text))

            if kat not in sttdt.keys():
                sttdt[kat] = dict()
            if deagd not in sttdt[kat].keys():
                sttdt[kat][deagd] = list()
            sttdt[kat][deagd].append(get_day_diff(row.find('sttdt').text, EXTRACT_DATE))

    for kat in deoff.keys():
        for deagd in deoff[kat].keys():
            target['fkk_instpln_head->' + kat + '->' + deagd + '->deoff->summe'] = round(sum(deoff[kat][deagd]), 2)
            target['fkk_instpln_head->' + kat + '->' + deagd + '->deoff->max'] = round(max(deoff[kat][deagd]), 2)
            if len(deoff[kat][deagd]) > 0:
                target['fkk_instpln_head->' + kat + '->' + deagd + '->deoff->durchschnitt'] = \
                    round(float(sum(deoff[kat][deagd]) / len(deoff[kat][deagd])), 2)

    for kat in ninst.keys():
        for deagd in ninst[kat].keys():
            if len(ninst[kat][deagd]) > 0:
                target['fkk_instpln_head->' + kat + '->' + deagd + '->ninst'] = \
                    round(float(sum(ninst[kat][deagd]) / len(ninst[kat][deagd])), 2)

    for kat in sttdt.keys():
        for deagd in sttdt[kat].keys():
            if len(sttdt[kat][deagd]) > 0:
                target['fkk_instpln_head->' + kat + '->' + deagd + '->anzahl'] = len(sttdt[kat][deagd])
                if len(list(filter(lambda d: d != 0, sttdt[kat][deagd]))) > 0:
                    target['fkk_instpln_head->' + kat + '->' + deagd + '->sttdt'] = \
                        max(filter(lambda d: d != 0, sttdt[kat][deagd]))

    return target


def transform_dfkkrk(table_rows: list):
    target = {'dfkkrk->re->valut': 0, 'dfkkrk->re->anzahl': 0,
              'dfkkrk->re->summh->summe': 0, 'dfkkrk->re->summh->max': 0, 'dfkkrk->re->summh->durchschnitt': 0,
              'dfkkrk->rc->valut': 0, 'dfkkrk->rc->anzahl': 0,
              'dfkkrk->rc->summh->summe': 0, 'dfkkrk->rc->summh->max': 0, 'dfkkrk->rc->summh->durchschnitt': 0
              }

    if len(table_rows) == 0:
        return target

    betraege = {'re': list(), 'rc': list()}
    daten = {'re': list(), 'rc': list()}
    for row in table_rows:
        blart = row.find('blart').text
        if blart is not None:
            blart = blart.lower()
            summh = row.find('summh').text
            valut = row.find('valut').text
            if summh is not None:
                betraege[blart].append(float(summh))

            if valut is not None:
                daten[blart].append(get_day_diff(valut, EXTRACT_DATE))

    for blart in betraege:
        if len(betraege[blart]) > 0:
            target['dfkkrk->' + blart + '->summh->summe'] = round(sum(betraege[blart]), 2)
            target['dfkkrk->' + blart + '->summh->max'] = round(max(betraege[blart]), 2)
            target['dfkkrk->' + blart + '->summh->durchschnitt'] = \
                round(float(sum(betraege[blart]) / len(betraege[blart])), 2)

    for blart in daten:
        if len(list(filter(lambda d: d != 0, daten[blart]))) > 0:
            target['dfkkrk->' + blart + '->valut'] = max(filter(lambda d: d != 0, daten[blart]))

        target['dfkkrk->' + blart + '->anzahl'] = len(daten[blart])

    return target


def transform_zdkk_crpo(table_rows: list):
    target = {'zdkk_crpo->betrw->summe': 0, 'zdkk_crpo->betrw->max': 0, 'zdkk_crpo->betrw->durchschnitt': 0,
              'zdkk_crpo->zzbudat': 0, 'zdkk_crpo->anzahl': 0}

    if len(table_rows) == 0:
        return target

    betraege = list()
    latest = 0
    for row in table_rows:
        betrw = row.find('betrw').text
        budat = row.find('zzbudat').text

        if betrw is not None:
            betraege.append(abs(float(betrw)))

        if budat is not None:
            dat = get_day_diff(budat, EXTRACT_DATE)
            if dat != 0 and (latest == 0 or dat < latest):
                latest = dat

    target['zdkk_crpo->zzbudat'] = latest
    if len(betraege) > 0:
        target['zdkk_crpo->anzahl'] = len(betraege)
        target['zdkk_crpo->betrw->summe'] = round(sum(betraege), 2)
        target['zdkk_crpo->betrw->max'] = round(max(betraege), 2)
        target['zdkk_crpo->betrw->durchschnitt'] = round(float(sum(betraege) / len(betraege)), 2)

    return target


def transform_zdkk_zv_azahl(table_rows: list):
    target = dict()

    rzawe = ['leer', '3', '4', 'v', 'w']
    paymmeth = ['leer', 'paypal', 'creditcard_computop']

    columns = ['rwbtr->summe', 'rwbtr->max', 'rwbtr->durchschnitt', 'anzahl']

    for weg in rzawe:
        for method in paymmeth:
            for c in columns:
                target['zdkk_zv_azahl->' + weg + '->' + method + '->' + c] = 0

    if len(table_rows) == 0:
        return target

    betraege = dict()
    for row in table_rows:
        weg = row.find('rzawe').text
        method = row.find('paymmeth').text
        rwbtr = row.find('rwbtr').text

        if weg is not None:
            weg = weg.lower()
        else:
            weg = 'leer'

        if method is not None:
            method = method.lower()
        else:
            method = 'leer'
        if rwbtr is not None:
            if weg not in betraege.keys():
                betraege[weg] = dict()

            if method not in betraege[weg].keys():
                betraege[weg][method] = list()

            betraege[weg][method].append(float(rwbtr))

    for weg in betraege.keys():
        for method in betraege[weg].keys():
            if len(betraege[weg][method]) > 0:
                target['zdkk_zv_azahl->' + weg + '->' + method + '->rwbtr->summe'] = \
                    round(sum(betraege[weg][method]), 2)
                target['zdkk_zv_azahl->' + weg + '->' + method + '->rwbtr->max'] = \
                    round(max(betraege[weg][method]), 2)
                target['zdkk_zv_azahl->' + weg + '->' + method + '->rwbtr->durchschnitt'] = \
                    round(float(sum(betraege[weg][method]) / len(betraege[weg][method])), 2)
                target['zdkk_zv_azahl->' + weg + '->' + method + '->anzahl'] = len(betraege[weg][method])

    return target


def transform_zdkk_dk_san_bas(table_rows: list):
    target = dict()

    sanktion = ['spg', 'nbea', 'mt', 'rku', 'spr', 'kuna', 'kung', 'vl']
    historie = ['aktuell', 'historie']
    columns = ['san_datum', 'betrag->summe', 'betrag->max', 'betrag->durchschnitt', 'anzahl']

    for san in sanktion:
        for his in historie:
            for c in columns:
                target['zdkk_dk_san_bas->' + san + '->' + his + '->' + c] = 0

    if len(table_rows) == 0:
        return target

    dates = dict()
    betraege = dict()
    for row in table_rows:
        san = row.find('sanktion').text
        if san is not None:
            san = san.lower()
            his = row.find('historie').text
            san_datum = row.find('san_datum').text
            betrag = row.find('betrag').text

            his = 'historie' if his is not None else 'aktuell'
            san_datum = get_day_diff(san_datum, EXTRACT_DATE) if san_datum is not None else 0
            betrag = float(betrag) if betrag is not None else 0.0

            if san not in dates.keys():
                dates[san] = dict()
            if his not in dates[san].keys():
                dates[san][his] = list()
            dates[san][his].append(san_datum)

            if san not in betraege.keys():
                betraege[san] = dict()
            if his not in betraege[san].keys():
                betraege[san][his] = list()
            betraege[san][his].append(betrag)

    for san in dates.keys():
        for his in dates[san].keys():
            filtered = list(filter(lambda d: d != 0, dates[san][his]))
            target['zdkk_dk_san_bas->' + san + '->' + his + '->anzahl'] = len(dates[san][his])
            target['zdkk_dk_san_bas->' + san + '->' + his + '->san_datum'] = min(filtered) if len(filtered) > 0 else 0

    for san in betraege.keys():
        for his in betraege[san].keys():
            if len(betraege[san][his]) > 0:
                target['zdkk_dk_san_bas->' + san + '->' + his + '->betrag->summe'] = \
                    round(sum(betraege[san][his]), 2)
                target['zdkk_dk_san_bas->' + san + '->' + his + '->betrag->max'] = \
                    round(max(betraege[san][his]), 2)
                target['zdkk_dk_san_bas->' + san + '->' + his + '->betrag->durchschnitt'] = \
                    round(float(sum(betraege[san][his]) / len(betraege[san][his])), 2)

    return target


def transform_fkk_sec(sek: list, sek_c=None):
    target = dict()

    reason = ['sl01', 'sl02', 'sl03', 'sl04', 'sl05', 'sl06', 'sl07',
              'sl08', 'sl09', 'sl11', 'sl12', 'sl13', 'sl98', 'sl99']
    rev_reason = ['leer', '0001', '0002', '0003', '0004']
    columns = ['anzahl',  'request->summe', 'request->max', 'request->durchschnitt']

    for grund in reason:
        for storno in rev_reason:
            for c in columns:
                target['fkk_sec->' + grund + '->' + storno + '->' + c] = 0

    if sek_c is None:
        sek_c = list()

    if len(sek) == 0 or len(sek_c) == 0:
        return target

    betraege = dict()
    for row in sek:
        row_id = row.find('security').text
        row_c = list(filter(lambda r: r.find('security').text == row_id, sek_c))
        if len(row_c) == 1:
            row_c = row_c[0]
        else:
            row_c = None

        grund = row.find('reason').text
        if grund is not None:
            grund = grund.lower()
            storno = row.find('rev_reason').text
            storno = storno.lower() if storno is not None else 'leer'

            if row_c is not None:
                betrag = row_c.find('request').text
                betrag = float(betrag) if betrag is not None else 0.0
            else:
                betrag = 0.0

            if grund not in betraege.keys():
                betraege[grund] = dict()
            if storno not in betraege[grund].keys():
                betraege[grund][storno] = list()

            betraege[grund][storno].append(betrag)

    for grund in betraege.keys():
        for storno in betraege[grund].keys():
            if len(betraege[grund][storno]) > 0:
                target['fkk_sec->' + grund + '->' + storno + '->anzahl'] = \
                    len(betraege[grund][storno])
                target['fkk_sec->' + grund + '->' + storno + '->request->summe'] = \
                    round(sum(betraege[grund][storno]), 2)
                target['fkk_sec->' + grund + '->' + storno + '->request->max'] = \
                    round(max(betraege[grund][storno]), 2)
                target['fkk_sec->' + grund + '->' + storno + '->request->durchschnitt'] = \
                    round(float(sum(betraege[grund][storno]) / len(betraege[grund][storno])), 2)

    return target


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
