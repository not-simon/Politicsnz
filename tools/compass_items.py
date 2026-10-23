#!/usr/bin/env python3
"""Item bank for the political-alignment ("compass") test (data/guide/compass.json).

Every item comes from an openly licensed psychometric instrument or a public cross-national
survey questionnaire. Wording is as published; where we adapted it (e.g. a 0-100 feeling
thermometer or a 1-10 bipolar scale rendered as a 5-point item) the adaptation is recorded.
Nothing here is taken from proprietary online compasses (politicalcompass.org, 8values, 9Axes,
SapplyValues, etc.).

direction: +1 = agreeing (or feeling positive) moves the respondent right / authoritarian-traditional
           / populist; -1 = reverse-keyed.
Build with:  python3 -I tools/compass_build.py
"""

# ---- sources ----------------------------------------------------------------
SECS = {
    'instrument': 'Social and Economic Conservatism Scale (SECS), 12 items',
    'citation': 'Everett, J. A. C. (2013). The 12 Item Social and Economic Conservatism Scale (SECS). PLoS ONE 8(12): e82131.',
    'url': 'https://doi.org/10.1371/journal.pone.0082131',
    'licence': 'CC0 1.0 (the article states the work is made available under the Creative Commons CC0 public domain dedication)',
    'original_format': 'Feeling thermometer: "How positive or negative do you feel about each issue on the scale of 0 to 100, where 0 represents very negative, and 100 represents very positive?"',
    'adaptation': 'Rendered as a 5-point item (very negative / negative / neutral / positive / very positive) mapped to -2..+2. Subscale membership (social 7 items, economic 5 items) follows Everett 2013, Table 4.',
    'archived_copy': 'raw/compass/secs_everett2013.html',
}
VSA = {
    'instrument': 'Very Short Authoritarianism (VSA) scale, 6 items',
    'citation': 'Bizumic, B., & Duckitt, J. (2018). Investigating Right Wing Authoritarianism With a Very Short Authoritarianism Scale. Journal of Social and Political Psychology, 6(1), 129-150.',
    'url': 'https://doi.org/10.5964/jspp.v6i1.835',
    'licence': 'CC BY 4.0 (journal licence statement on the article page)',
    'original_format': 'Agree/disagree items; the authors used a nine-point Likert-type scale in their studies.',
    'adaptation': '5-point agree/disagree scale instead of the nine-point scale. Wording verbatim from Appendix A (the published text reads "if we are going preserve law and order"; we keep that sentence as written).',
    'archived_copy': 'raw/compass/vsa_bizumic2018.html',
}
CSES5 = {
    'instrument': 'Comparative Study of Electoral Systems (CSES) Module 5 (2016-2021) questionnaire',
    'citation': 'The Comparative Study of Electoral Systems (www.cses.org). CSES Module 5 Questionnaire (final, 2016). Variables Q04a-Q04g (attitudes about elites), Q05b-Q05d (out-group attitudes), Q08 (government action on income differences).',
    'url': 'https://cses.org/wp-content/uploads/2019/05/cses5_Questionnaire.txt',
    'licence': 'CSES data and documentation are made freely available for research and educational use with citation (cses.org data-download terms); the questionnaire is a public document. New Zealand fielded Module 5 in the 2017 and 2020 NZES.',
    'original_format': '5-point: strongly agree / somewhat agree / neither / somewhat disagree / strongly disagree.',
    'adaptation': '[COUNTRY] replaced with "New Zealand". Otherwise verbatim.',
    'archived_copy': 'raw/compass/cses5_Questionnaire.txt',
}
WVS7 = {
    'instrument': 'World Values Survey Wave 7 (2017-2022) master questionnaire',
    'citation': 'Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. World Values Survey: Round Seven. WVS Wave 7 Master Survey Questionnaire, items Q106-Q109 (economic values).',
    'url': 'https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp',
    'licence': 'WVS questionnaires and data are published free of charge for non-commercial research use with citation (worldvaluessurvey.org). Copy used: Wave 7 master questionnaire as fielded in Great Britain (IHSN catalogue 12279).',
    'original_format': 'Bipolar 1-10 scale between two opposed statements ("Incomes should be made more equal" vs "There should be greater incentives for individual effort", etc.).',
    'adaptation': 'One pole of each bipolar item is used as a 5-point agree/disagree statement; the opposing pole is recorded in the item notes so the method page can show it.',
    'archived_copy': 'raw/compass/wvs7_master_questionnaire.pdf',
}
ESS = {
    'instrument': 'European Social Survey (ESS) core questionnaire, Round 9 (2018) source questionnaire',
    'citation': 'European Social Survey Round 9 Source Questionnaire (2018). Core item B34 (variable freehms). The same item has been asked in every ESS round since 2002.',
    'url': 'https://www.europeansocialsurvey.org/docs/round9/fieldwork/source/ESS9_source_questionnaires.pdf',
    'licence': 'ESS documentation is licensed under CC BY-SA 4.0 (europeansocialsurvey.org conditions of use); ESS data under CC BY-NC-SA 4.0.',
    'original_format': '5-point: agree strongly / agree / neither / disagree / disagree strongly.',
    'adaptation': 'None (footnote 15 of the source questionnaire is omitted).',
    'archived_copy': 'raw/compass/ESS9_source_questionnaires.pdf',
}
NZES23 = {
    'instrument': 'New Zealand Election Study 2023 mass survey questionnaire',
    'citation': 'Vowles, J. et al. (2024). The 2023 New Zealand Election Study: questionnaire. Items C6c and C12e (section C, "Your opinions").',
    'url': 'https://www.nzes.net/files/2024/03/2023-NZESFinal-d23f98922870a844.pdf',
    'licence': 'Publicly posted questionnaire (nzes.net). Reused as a standard research instrument with citation; NZES unit-record data are subject to the NZES Data Usage Terms and are not used here.',
    'original_format': '5-point: strongly agree / somewhat agree / neither / somewhat disagree / strongly disagree.',
    'adaptation': 'None.',
    'archived_copy': 'raw/compass/nzes2023_questionnaire.pdf',
}

SCALE_LIKERT = {
    'type': 'likert5',
    'labels': ['Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree'],
    'values': [-2, -1, 0, 1, 2],
}
SCALE_THERMO = {
    'type': 'feeling5',
    'prompt': 'How positive or negative do you feel about:',
    'labels': ['Very negative', 'Negative', 'Neutral', 'Positive', 'Very positive'],
    'values': [-2, -1, 0, 1, 2],
    'note': 'Adapted from the SECS 0-100 feeling thermometer.',
}

ITEMS = []

def I(id, axis, direction, text, source, subscale, item_ref=None, note=None, scale=SCALE_LIKERT):
    ITEMS.append({
        'id': id, 'axis': axis, 'direction': direction, 'text': text,
        'subscale': subscale, 'item_ref': item_ref, 'note': note,
        'scale': scale, 'source': source,
    })

# =============================================================== ECONOMIC (12; 6 keyed right, 6 keyed left)
I('econ_wvs_incomes', 'economic', -1, 'Incomes should be made more equal.', WVS7, 'wvs_economic_values',
  'Q106 (pole 1)', 'Opposing pole in WVS: "There should be greater incentives for individual effort."')
I('econ_wvs_ownership', 'economic', +1, 'Private ownership of business and industry should be increased.', WVS7, 'wvs_economic_values',
  'Q107 (pole 1)', 'Opposing pole in WVS: "Government ownership of business and industry should be increased."')
I('econ_wvs_responsibility', 'economic', -1, 'Government should take more responsibility to ensure that everyone is provided for.', WVS7, 'wvs_economic_values',
  'Q108 (pole 1)', 'Opposing pole in WVS: "People should take more responsibility to provide for themselves."')
I('econ_wvs_competition', 'economic', +1, 'Competition is good.', WVS7, 'wvs_economic_values',
  'Q109 (pole 1)', 'Opposing pole in WVS: "Competition is harmful." The Wave 7 master questionnaire fielded in Great Britain gives only these short pole labels.')
I('econ_cses_reduce_differences', 'economic', -1, 'The government should take measures to reduce differences in income levels.', CSES5, 'cses_redistribution',
  'Q08', 'Identical wording is used in ESS core item B33 (gincdif) and NZES 2023 item C6a, so NZ population benchmarks exist.')
I('econ_nzes_privatisation', 'economic', -1, 'Privatisation of state-owned enterprises has gone too far.', NZES23, 'nzes_economic',
  'C6c', 'Long-running NZES item (asked since the 1990s).')
I('econ_nzes_big_business', 'economic', -1, 'Big business in New Zealand has too much power.', NZES23, 'nzes_economic',
  'C12e', None)
I('econ_secs_limited_government', 'economic', +1, 'Limited government', SECS, 'secs_economic', 'SECS item 5', None, SCALE_THERMO)
I('econ_secs_welfare_benefits', 'economic', -1, 'Welfare benefits', SECS, 'secs_economic', 'SECS item 2 (reverse scored)', None, SCALE_THERMO)
I('econ_secs_business', 'economic', +1, 'Business', SECS, 'secs_economic', 'SECS item 12', None, SCALE_THERMO)
I('econ_secs_fiscal_responsibility', 'economic', +1, 'Fiscal responsibility', SECS, 'secs_economic', 'SECS item 11', None, SCALE_THERMO)
# SECS item 8 (gun ownership) omitted: a US-specific item with no NZ political meaning (flagged by coder).

# =============================================================== SOCIAL: GAL-TAN / libertarian-authoritarian (16; 10 keyed TAN, 6 keyed GAL)
I('soc_vsa_defy_authority', 'social', -1, "It's great that many young people today are prepared to defy authority.", VSA, 'vsa_authoritarianism',
  'VSA item 1 (Conservatism / Authoritarian Submission; reverse scored)', None)
I('soc_vsa_discipline', 'social', +1, 'What our country needs most is discipline, with everyone following our leaders in unity.', VSA, 'vsa_authoritarianism',
  'VSA item 2 (Conservatism / Authoritarian Submission)', None)
I('soc_vsa_gods_laws', 'social', +1, "God's laws about abortion, pornography, and marriage must be strictly followed before it is too late.", VSA, 'vsa_authoritarianism',
  'VSA item 3 (Traditionalism / Conventionalism)', None)
I('soc_vsa_premarital', 'social', -1, 'There is nothing wrong with premarital sexual intercourse.', VSA, 'vsa_authoritarianism',
  'VSA item 4 (Traditionalism / Conventionalism; reverse scored)', None)
I('soc_vsa_not_tougher', 'social', -1, 'Our society does NOT need tougher government and stricter laws.', VSA, 'vsa_authoritarianism',
  'VSA item 5 (Authoritarianism / Authoritarian Aggression; reverse scored)', None)
I('soc_vsa_crack_down', 'social', +1, 'The facts on crime and the recent public disorders show we have to crack down harder on troublemakers, if we are going preserve law and order.', VSA, 'vsa_authoritarianism',
  'VSA item 6 (Authoritarianism / Authoritarian Aggression)', 'Wording exactly as printed in Appendix A of Bizumic & Duckitt (2018).')
I('soc_secs_abortion', 'social', -1, 'Abortion', SECS, 'secs_social', 'SECS item 1 (reverse scored)', None, SCALE_THERMO)
I('soc_secs_religion', 'social', +1, 'Religion', SECS, 'secs_social', 'SECS item 7', None, SCALE_THERMO)
I('soc_secs_traditional_marriage', 'social', +1, 'Traditional marriage', SECS, 'secs_social', 'SECS item 9', None, SCALE_THERMO)
I('soc_secs_traditional_values', 'social', +1, 'Traditional values', SECS, 'secs_social', 'SECS item 10', None, SCALE_THERMO)
I('soc_secs_family_unit', 'social', +1, 'The family unit', SECS, 'secs_social', 'SECS item 13', None, SCALE_THERMO)
I('soc_secs_patriotism', 'social', +1, 'Patriotism', SECS, 'secs_social', 'SECS item 14', None, SCALE_THERMO)
I('soc_secs_military', 'social', +1, 'Military and national security', SECS, 'secs_social', 'SECS item 6', None, SCALE_THERMO)
I('soc_ess_gay_free', 'social', -1, 'Gay men and lesbians should be free to live their own life as they wish.', ESS, 'ess_social_values', 'B34 (freehms)', None)
I('soc_cses_immigrants_economy', 'social', -1, "Immigrants are generally good for New Zealand's economy.", CSES5, 'cses_outgroup', 'Q05c', '[COUNTRY] = New Zealand.')
I('soc_cses_culture_harmed', 'social', +1, "New Zealand's culture is generally harmed by immigrants.", CSES5, 'cses_outgroup', 'Q05d', '[COUNTRY] = New Zealand.')

# =============================================================== POPULISM / anti-establishment (8; 7 keyed populist, 1 reverse)
I('pop_cses_compromise', 'populism', +1, "What people call compromise in politics is really just selling out on one's principles.", CSES5, 'cses_populism', 'Q04a', None)
I('pop_cses_dont_care', 'populism', +1, 'Most politicians do not care about the people.', CSES5, 'cses_populism', 'Q04b', None)
I('pop_cses_trustworthy', 'populism', -1, 'Most politicians are trustworthy.', CSES5, 'cses_populism', 'Q04c (reverse scored)', None)
I('pop_cses_main_problem', 'populism', +1, 'Politicians are the main problem in New Zealand.', CSES5, 'cses_populism', 'Q04d', '[COUNTRY] = New Zealand.')
I('pop_cses_strong_leader', 'populism', +1, 'Having a strong leader in government is good for New Zealand even if the leader bends the rules to get things done.', CSES5, 'cses_populism', 'Q04e', '[COUNTRY] = New Zealand.')
I('pop_cses_people_decide', 'populism', +1, 'The people, and not politicians, should make our most important policy decisions.', CSES5, 'cses_populism', 'Q04f', None)
I('pop_cses_rich_powerful', 'populism', +1, 'Most politicians care only about the interests of the rich and powerful.', CSES5, 'cses_populism', 'Q04g', None)
I('pop_cses_majority', 'populism', +1, 'The will of the majority should always prevail, even over the rights of minorities.', CSES5, 'cses_antipluralism', 'Q05b',
  'Kept on the populism axis as its anti-pluralist component (Mudde 2004; the Global Party Survey populism definition); not part of the CSES Q04 elite battery.')

AXES = {
    'economic': {
        'label': 'Economic left-right',
        'left_pole': 'Left: state intervention, redistribution, public ownership',
        'right_pole': 'Right: markets, limited government, fiscal restraint',
        'basis': 'Hooghe, Marks & Wilson (2002) economic left-right; CHES "lrecon"; Global Party Survey V4.',
        'min_items': 6,
    },
    'social': {
        'label': 'Social: libertarian/green-alternative (GAL) to traditional/authoritarian/nationalist (TAN)',
        'left_pole': 'GAL / libertarian: personal freedom, pluralism, openness',
        'right_pole': 'TAN / authoritarian: order, tradition, national culture',
        'basis': 'Hooghe, Marks & Wilson (2002) GAL-TAN; Kitschelt (1994) libertarian-authoritarian; CHES "galtan"; Global Party Survey V6.',
        'min_items': 8,
    },
    'populism': {
        'label': 'Populist / anti-establishment attitudes',
        'left_pole': 'Pluralist: trusts representative institutions, compromise, minority rights',
        'right_pole': 'Populist: people vs. elite, popular sovereignty, anti-politician',
        'basis': 'Mudde (2004); Akkerman, Mudde & Zaslove (2014); CSES Module 5 "Democracy Divided?" elite battery; Global Party Survey V8.',
        'min_items': 4,
    },
}
