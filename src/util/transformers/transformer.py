from transformer_table import *


class Transformer:

    __map_table_transformer = {
        'but000': TransformerBut000,
        'zdkk_rb_scores': TransformerZdkk_rb_scores,
        'zdkk_sb_gp_azam': TransformerZdkk_sb_gp_azam,
        'ekun': TransformerEkun,
        'dfkkko': TransformerDfkkko,
        'dfkkop': TransformerDfkkop,
        'but0bk': TransformerBut0bk,
        'fkkmaze': TransformerFkkmaze,
        'fkkmako': TransformerFkkmako,
        'tiban': TransformerTiban,
        'dfkklocks': TransformerDfkklocks,
        'zdkk_mw_vtref_st': TransformerZdkk_mw_vtref_st,
        'dfkkcohi': TransformerDfkkcohi,
        'dfkklocksh': TransformerDfkklocksh,
        'dfkkcoh': TransformerDfkkcoh,
        'zdkk_mwk_xml_snd': TransformerZdkk_mwk_xml_snd,
        'zdkk_mwk_xml_dok': TransformerZdkk_mwk_xml_dok,
        'zdkk_mwk_xml_cor': TransformerZdkk_mwk_xml_cor,
        'zdkk_mwk_xml_pos': TransformerZdkk_mwk_xml_pos,
        'zdkk_abg_vors': TransformerZdkk_abg_vors,
        'dfkkzk': TransformerDfkkzk,
        'dfkkzp': TransformerDfkkzp,
        'sepa_mandate': TransformerSepa_mandate,
        'dfkkwoh': TransformerDfkkwoh,
        'zdkk_rb_ausb': TransformerZdkk_rb_ausb,
        'zdkk_ba_fv_ausb': TransformerZdkk_ba_fv_ausb,
        'zdkk_abg_ausb_po': TransformerZdkk_abg_ausb_po,
        'zdkk_abg_ink': TransformerZdkk_abg_ink,
        'zdkk_rb_ereignis': TransformerZdkk_rb_ereignis,
        'zdkk_mw_ribs_cmo': TransformerZdkk_mw_ribs_cmo,
        'dfkkrapt': TransformerDfkkrapt,
        'dfkkrat': TransformerDfkkrat,
        'zdkk_rechb1_bas': TransformerZdkk_rechb1_bas,
        'zdkk_im_inkstat': TransformerZdkk_im_inkstat,
        'dpayh': TransformerDpayh,
        'dpayp': TransformerDpayp,
        'fkk_instpln_head': TransformerFkk_instpln_head,
        'fkk_instpln_hist': TransformerFkk_instpln_hist,
        'zdkk_sb_vv_vt': TransformerZdkk_sb_vv_vt,
        'zdkk_mw_dkb_list': TransformerZdkk_mw_dkb_list,
        'dfkkrk': TransformerDfkkrk,
        'dfkkrp': TransformerDfkkrp,
        'zdkk_dk_rk_rp': TransformerZdkk_dk_rk_rp,
        'dfkkrh': TransformerDfkkrh,
        'zdkk_rp_typ_map': TransformerZdkk_rp_typ_map,
        'sepa_mandate_use': TransformerSepa_mandate_use,
        'zdkk_mw_mhn_ads': TransformerZdkk_mw_mhn_ads,
        'zdkk_bapi_obcfc': TransformerZdkk_bapi_obcfc,
        'fkkmakt': TransformerFkkmakt,
        'zdkk_bapi_obbel': TransformerZdkk_bapi_obbel,
        'zdkk_zv_azahl': TransformerZdkk_zv_azahl,
        'zdkk_debdel': TransformerZdkk_debdel,
        'zdkk_dfkkdda': TransformerZdkk_dfkkdda,
        'zdkk_instplnhis2': TransformerZdkk_instplnhis2,
        'zdkk_instplnhist': TransformerZdkk_instplnhist,
        'zdkk_crpo': TransformerZdkk_crpo,
        'zdkk_dk_san_bas': TransformerZdkk_dk_san_bas,
        'dfkkcfzst': TransformerDfkkcfzst,
        'zdkk_abg_n_cfc': TransformerZdkk_abg_n_cfc,
        'fkk_sec': TransformerFkk_sec,
        'fkk_sec_c': TransformerFkk_sec_c,
        'zdkk_mw_vtref_sh': TransformerZdkk_mw_vtref_sh,
        'dfkkzpe': TransformerDfkkzpe,
        'dfkkcrh': TransformerDfkkcrh,
        'zdkk_rb_st_vkont': TransformerZdkk_rb_st_vkont
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
