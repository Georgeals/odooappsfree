# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2020-TODAY ArtLineStudio(<https://artlinespb.ru/>).
#    Author: George Yanguzov(<george@artlinespb.ru>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Russian document - UTD",
    "summary": """
        Russian document - Unified Transfer Document
        
        """,
    "description": """
        Russian document - Unified Transfer Document
        
        10.0.0.2 - Обновление формы УПД от 01.07.2021
        
        10.0.0.3 - Fix: отображение корректных данных при выборе контактного лица компании.""",
    "author": "ArtLine",
    "company": "ArtLineStudio LTD",
    "website": "https://artlinespb.ru/",
    "category": "Localization",
    "version": "17.0.0.0",
    "depends": ["base", "l10n_ru_doc"],
    "data": [
        "report/report.xml",
        "report/template.xml",
        # "report/template_bak.xml",
        "report/basic_templates.xml",
        "res_company_views.xml",
    ],
}
