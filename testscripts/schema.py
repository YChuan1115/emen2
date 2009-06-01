from test import *

#begin parameter: reference
reference =  Database.ParamDef()
reference.name = 'reference'
reference.vartype = 'int'
reference.desc_short = '''A reference to another record by id'''
db.addparamdef(reference,ctxid)
#end parameter: reference

#begin parameter: indexby
indexby =  Database.ParamDef()
indexby.name = 'indexby'
indexby.vartype = 'string'
indexby.desc_short = '''a string used to retrieve records'''
db.addparamdef(indexby,ctxid)
#end parameter: indexby

#begin parameter: template
template =  Database.ParamDef()
template.name = 'template'
template.vartype = 'string'
template.desc_short = '''a string used to retrieve records'''
db.addparamdef(template,ctxid)
#end parameter: template

#begin parameter: template_name
template_name =  Database.ParamDef()
template_name.name = 'template_name'
template_name.vartype = 'string'
template_name.desc_short = '''the template of the current record'''
db.addparamdef(template_name,ctxid)
#end parameter: template_name

#begin parameter: event_name
event_name =  Database.ParamDef()
event_name.name = 'event_name'
event_name.vartype = 'string'
event_name.desc_short = '''The name of the event'''
db.addparamdef(event_name,ctxid)
#end parameter: event_name

#begin parameter: event_date
event_date =  Database.ParamDef()
event_date.name = 'event_date'
event_date.vartype = 'datetime'
event_date.desc_short = '''The date of the event'''
db.addparamdef(event_date,ctxid)
#end parameter: event_date

#begin parameter: event_agenda
event_agenda =  Database.ParamDef()
event_agenda.name = 'event_agenda'
event_agenda.vartype = 'text'
event_agenda.desc_short = '''The event's agenda'''
db.addparamdef(event_agenda,ctxid)
#end parameter: event_agenda

#begin record definition: event
event = Database.RecordDef()
event.name = 'event'
event.mainview = """$$event_name<br />$$event_date<br />$$event_agenda"""
event.views['tabularview'] = """$$event_name $$event_date"""
event.views['defaultview'] = """$$event_name on $$event_date"""
event.views['recname'] = """$$event_name"""
db.addrecorddef(event,ctxid)
#end record definition: event

#begin parameter: presentation_presenter
presentation_presenter =  Database.ParamDef()
presentation_presenter.name = 'presentation_presenter'
presentation_presenter.vartype = 'user'
presentation_presenter.desc_short = '''The person making the presentation'''
db.addparamdef(presentation_presenter,ctxid)
#end parameter: presentation_presenter

#begin parameter: presentation_title
presentation_title =  Database.ParamDef()
presentation_title.name = 'presentation_title'
presentation_title.vartype = 'string'
presentation_title.desc_short = '''The title of the presentation'''
db.addparamdef(presentation_title,ctxid)
#end parameter: presentation_title

#begin parameter: presentation_file
presentation_file =  Database.ParamDef()
presentation_file.name = 'presentation_file'
presentation_file.vartype = 'binary'
presentation_file.desc_short = '''The presentation's slides'''
db.addparamdef(presentation_file,ctxid)
#end parameter: presentation_file

#begin record definition: presentation
presentation = Database.RecordDef()
presentation.name = 'presentation'
presentation.mainview = """$$presentation_presenter<br />$$presentation_title<br />$$presentation_file some more stuff... continued"""
presentation.views['tabularview'] = """$$presentation_presenter $$presentation_title"""
presentation.views['defaultview'] = """$$presentation_title presented by $$presentation_presenter"""
presentation.views['recname'] = """$$presentation_title"""
db.addrecorddef(presentation,ctxid)
#end record definition: presentation

#begin parameter: sponsor_name
sponsor_name =  Database.ParamDef()
sponsor_name.name = 'sponsor_name'
sponsor_name.vartype = 'string'
sponsor_name.desc_short = '''The sponsor's name'''
db.addparamdef(sponsor_name,ctxid)
#end parameter: sponsor_name

#begin parameter: sponsor_website
sponsor_website =  Database.ParamDef()
sponsor_website.name = 'sponsor_website'
sponsor_website.vartype = 'string'
sponsor_website.desc_short = '''The sponsor's website'''
db.addparamdef(sponsor_website,ctxid)
#end parameter: sponsor_website

#begin parameter: sponsor_logo
sponsor_logo =  Database.ParamDef()
sponsor_logo.name = 'sponsor_logo'
sponsor_logo.vartype = 'binaryimage'
sponsor_logo.desc_short = '''The sponsor's logo'''
db.addparamdef(sponsor_logo,ctxid)
#end parameter: sponsor_logo

#begin record definition: sponsor
sponsor = Database.RecordDef()
sponsor.name = 'sponsor'
sponsor.mainview = """$$sponsor_name<br />$$sponsor_website<br />$$sponsor_logo"""
sponsor.views['tabularview'] = """$$sponsor_name $$sponsor_website"""
sponsor.views['defaultview'] = """<a href="$$sponsor_website">$$sponsor_name</a>"""
sponsor.views['recname'] = """$$sponsor_name"""
db.addrecorddef(sponsor,ctxid)
#end record definition: sponsor

#begin parameter: location_name
location_name =  Database.ParamDef()
location_name.name = 'location_name'
location_name.vartype = 'string'
location_name.desc_short = '''The name of the location'''
db.addparamdef(location_name,ctxid)
#end parameter: location_name

#begin parameter: location_address
location_address =  Database.ParamDef()
location_address.name = 'location_address'
location_address.vartype = 'string'
location_address.desc_short = '''The address of the location'''
db.addparamdef(location_address,ctxid)
#end parameter: location_address

#begin record definition: location
location = Database.RecordDef()
location.name = 'location'
location.mainview = """$$location_name<br />$$location_address"""
location.views['tabularview'] = """$$location_name"""
location.views['defaultview'] = """$$location_name"""
location.views['recname'] = """$$location_name"""
db.addrecorddef(location,ctxid)
#end record definition: location

#begin parameter: folder_name
folder_name =  Database.ParamDef()
folder_name.name = 'folder_name'
folder_name.vartype = 'string'
folder_name.desc_short = '''The name of a folder'''
db.addparamdef(folder_name,ctxid)
#end parameter: folder_name

#begin record definition: folder
folder = Database.RecordDef()
folder.name = 'folder'
folder.mainview = """$$folder_name"""
folder.views['tabularview'] = """$$folder_name"""
folder.views['defaultview'] = """$$folder_name"""
folder.views['recname'] = """$$folder_name"""
db.addrecorddef(folder,ctxid)
#end record definition: folder

#begin parameter: template_name
template_name =  Database.ParamDef()
template_name.name = 'template_name'
template_name.vartype = 'string'
template_name.desc_short = '''the name of the template'''
db.addparamdef(template_name,ctxid)
#end parameter: template_name

#begin parameter: template_template
template_template =  Database.ParamDef()
template_template.name = 'template_template'
template_template.vartype = 'text'
template_template.desc_short = '''the template's context'''
db.addparamdef(template_template,ctxid)
#end parameter: template_template

#begin record definition: template
template = Database.RecordDef()
template.name = 'template'
template.mainview = """$$template_name $$template_template"""
template.views['tabularview'] = """$$template_name"""
template.views['defaultview'] = """$$template_name<br />$$template_template"""
template.views['recname'] = """$$template_name"""
db.addrecorddef(template,ctxid)
#end record definition: template

#begin parameter: project_name
project_name =  Database.ParamDef()
project_name.name = 'project_name'
project_name.vartype = 'string'
project_name.desc_short = '''project title'''
db.addparamdef(project_name,ctxid)
#end parameter: project_name

#begin parameter: project_dates
project_dates =  Database.ParamDef()
project_dates.name = 'project_dates'
project_dates.vartype = 'string'
project_dates.desc_short = '''project dates'''
db.addparamdef(project_dates,ctxid)
#end parameter: project_dates

#begin parameter: project_type
project_type =  Database.ParamDef()
project_type.name = 'project_type'
project_type.vartype = 'string'
project_type.desc_short = '''type of project'''
db.addparamdef(project_type,ctxid)
#end parameter: project_type

#begin parameter: project_description
project_description =  Database.ParamDef()
project_description.name = 'project_description'
project_description.vartype = 'text'
project_description.desc_short = '''project description'''
db.addparamdef(project_description,ctxid)
#end parameter: project_description

#begin parameter: project_reprints
project_reprints =  Database.ParamDef()
project_reprints.name = 'project_reprints'
project_reprints.vartype = 'text'
project_reprints.desc_short = '''reprints/publications of the project'''
db.addparamdef(project_reprints,ctxid)
#end parameter: project_reprints

#begin record definition: project
project = Database.RecordDef()
project.name = 'project'
project.mainview = """$$project_name $$project_dates $$project_type $$project_description $$project_reprints"""
project.views['tabularview'] = """$$project_name"""
project.views['defaultview'] = """$$project_name"""
project.views['recname'] = """$$project_name"""
db.addrecorddef(project,ctxid)
#end record definition: project

#begin parameter: grant_agency_name
grant_agency_name =  Database.ParamDef()
grant_agency_name.name = 'grant_agency_name'
grant_agency_name.vartype = 'string'
grant_agency_name.desc_short = '''Name of the Grant Agency'''
db.addparamdef(grant_agency_name,ctxid)
#end parameter: grant_agency_name

#begin parameter: grant_number
grant_number =  Database.ParamDef()
grant_number.name = 'grant_number'
grant_number.vartype = 'int'
grant_number.desc_short = '''Grant Number'''
db.addparamdef(grant_number,ctxid)
#end parameter: grant_number

#begin parameter: grant_title
grant_title =  Database.ParamDef()
grant_title.name = 'grant_title'
grant_title.vartype = 'string'
grant_title.desc_short = '''Grant Title'''
db.addparamdef(grant_title,ctxid)
#end parameter: grant_title

#begin parameter: grant_duration
grant_duration =  Database.ParamDef()
grant_duration.name = 'grant_duration'
grant_duration.vartype = 'string'
grant_duration.desc_short = '''Grant Duration'''
db.addparamdef(grant_duration,ctxid)
#end parameter: grant_duration

#begin parameter: grant_total_cost
grant_total_cost =  Database.ParamDef()
grant_total_cost.name = 'grant_total_cost'
grant_total_cost.vartype = 'float'
grant_total_cost.desc_short = '''Grant Total Cost'''
db.addparamdef(grant_total_cost,ctxid)
#end parameter: grant_total_cost

#begin record definition: grant
grant = Database.RecordDef()
grant.name = 'grant'
grant.mainview = """$$grant_agency_name $$grant_number $$grant_title $$grant_duration $$grant_total_cost"""
grant.views['tabularview'] = """$$grant_title from $$grant_agency_name"""
grant.views['defaultview'] = """$$grant_title"""
grant.views['recname'] = """$$grant_title"""
db.addrecorddef(grant,ctxid)
#end record definition: grant

#begin parameter: person_name
person_name =  Database.ParamDef()
person_name.name = 'person_name'
person_name.vartype = 'string'
person_name.desc_short = '''Name'''
db.addparamdef(person_name,ctxid)
#end parameter: person_name

#begin parameter: person_metaname
person_metaname =  Database.ParamDef()
person_metaname.name = 'person_metaname'
person_metaname.vartype = 'string'
person_metaname.desc_short = '''Unique Identifier'''
db.addparamdef(person_metaname,ctxid)
#end parameter: person_metaname

#begin parameter: person_degrees
person_degrees =  Database.ParamDef()
person_degrees.name = 'person_degrees'
person_degrees.vartype = 'string'
person_degrees.desc_short = '''Degrees'''
db.addparamdef(person_degrees,ctxid)
#end parameter: person_degrees

#begin parameter: person_department
person_department =  Database.ParamDef()
person_department.name = 'person_department'
person_department.vartype = 'string'
person_department.desc_short = '''Department'''
db.addparamdef(person_department,ctxid)
#end parameter: person_department

#begin parameter: person_institution
person_institution =  Database.ParamDef()
person_institution.name = 'person_institution'
person_institution.vartype = 'string'
person_institution.desc_short = '''Institution'''
db.addparamdef(person_institution,ctxid)
#end parameter: person_institution

#begin parameter: person_phone
person_phone =  Database.ParamDef()
person_phone.name = 'person_phone'
person_phone.vartype = 'string'
person_phone.desc_short = '''Phone Number'''
db.addparamdef(person_phone,ctxid)
#end parameter: person_phone

#begin parameter: person_email
person_email =  Database.ParamDef()
person_email.name = 'person_email'
person_email.vartype = 'string'
person_email.desc_short = '''Email Address'''
db.addparamdef(person_email,ctxid)
#end parameter: person_email

#begin parameter: person_fax
person_fax =  Database.ParamDef()
person_fax.name = 'person_fax'
person_fax.vartype = 'string'
person_fax.desc_short = '''Fax'''
db.addparamdef(person_fax,ctxid)
#end parameter: person_fax

#begin parameter: person_photo
person_photo =  Database.ParamDef()
person_photo.name = 'person_photo'
person_photo.vartype = 'binaryimage'
person_photo.desc_short = '''A Photo'''
db.addparamdef(person_photo,ctxid)
#end parameter: person_photo

#begin record definition: person
person = Database.RecordDef()
person.name = 'person'
person.mainview = """$$person_name $$person_degrees $$person_department  $$person_institution $$person_phone $$person_fax $$person_email"""
person.views['tabularview'] = """$$person_name"""
person.views['defaultview'] = """$$person_name"""
person.views['recname'] = """$$person_name"""
db.addrecorddef(person,ctxid)
#end record definition: person

#begin parameter: address_top
address_top =  Database.ParamDef()
address_top.name = 'address_top'
address_top.vartype = 'string'
address_top.desc_short = '''Address Top Line(s)'''
db.addparamdef(address_top,ctxid)
#end parameter: address_top

#begin parameter: address_city
address_city =  Database.ParamDef()
address_city.name = 'address_city'
address_city.vartype = 'string'
address_city.desc_short = '''City'''
db.addparamdef(address_city,ctxid)
#end parameter: address_city

#begin parameter: address_state
address_state =  Database.ParamDef()
address_state.name = 'address_state'
address_state.vartype = 'string'
address_state.desc_short = '''State'''
db.addparamdef(address_state,ctxid)
#end parameter: address_state

#begin parameter: address_zip
address_zip =  Database.ParamDef()
address_zip.name = 'address_zip'
address_zip.vartype = 'string'
address_zip.desc_short = '''Zipcode'''
db.addparamdef(address_zip,ctxid)
#end parameter: address_zip

#begin parameter: address_country
address_country =  Database.ParamDef()
address_country.name = 'address_country'
address_country.vartype = 'string'
address_country.desc_short = '''Country'''
db.addparamdef(address_country,ctxid)
#end parameter: address_country

#begin record definition: address
address = Database.RecordDef()
address.name = 'address'
address.mainview = """$$address_top<br />$$address_city,$$address_state $$address_zip<br />$$address_country"""
address.views['tabularview'] = """$$address_top"""
address.views['defaultview'] = """$$address_top"""
address.views['recname'] = """$$address_top"""
db.addrecorddef(address,ctxid)
#end record definition: address

#begin parameter: menu_label
menu_label =  Database.ParamDef()
menu_label.name = 'menu_label'
menu_label.vartype = 'string'
menu_label.desc_short = '''Displayed menu item name'''
db.addparamdef(menu_label,ctxid)
#end parameter: menu_label

#begin parameter: menu_link
menu_link =  Database.ParamDef()
menu_link.name = 'menu_link'
menu_link.vartype = 'string'
menu_link.desc_short = '''Menu Item target'''
db.addparamdef(menu_link,ctxid)
#end parameter: menu_link

#begin parameter: menu_name
menu_name =  Database.ParamDef()
menu_name.name = 'menu_name'
menu_name.vartype = 'string'
menu_name.desc_short = '''The name of the URL to look up'''
db.addparamdef(menu_name,ctxid)
#end parameter: menu_name

#begin parameter: menu_arguments
menu_arguments =  Database.ParamDef()
menu_arguments.name = 'menu_arguments'
menu_arguments.vartype = 'string'
menu_arguments.desc_short = '''A pickle of the arguments to pass'''
db.addparamdef(menu_arguments,ctxid)
#end parameter: menu_arguments

#begin record definition: menu_item
menu_item = Database.RecordDef()
menu_item.name = 'menu_item'
menu_item.mainview = """$$menu_label $$menu_link"""
menu_item.views['tabularview'] = """$$menu_label"""
menu_item.views['defaultview'] = """$$menu_label"""
menu_item.views['recname'] = """$$menu_label"""
db.addrecorddef(menu_item,ctxid)
#end record definition: menu_item

#begin parameter: page_name
page_name =  Database.ParamDef()
page_name.name = 'page_name'
page_name.vartype = 'string'
page_name.desc_short = '''Page Name'''
db.addparamdef(page_name,ctxid)
#end parameter: page_name

#begin parameter: page_menus
page_menus =  Database.ParamDef()
page_menus.name = 'page_menus'
page_menus.vartype = 'string'
page_menus.desc_short = '''Page Menus'''
db.addparamdef(page_menus,ctxid)
#end parameter: page_menus

#begin parameter: page_content
page_content =  Database.ParamDef()
page_content.name = 'page_content'
page_content.vartype = 'text'
page_content.desc_short = '''Page Content'''
db.addparamdef(page_content,ctxid)
#end parameter: page_content

#begin record definition: page
page = Database.RecordDef()
page.name = 'page'
page.mainview = """$$page_name $$page_menus $$page_content"""
page.views['tabularview'] = """$$page_name"""
page.views['defaultview'] = """$$page_name $$page_menus $$page_content"""
page.views['recname'] = """$$page_name"""
db.addrecorddef(page,ctxid)
#end record definition: page

#begin parameter: schedule_times
schedule_times =  Database.ParamDef()
schedule_times.name = 'schedule_times'
schedule_times.vartype = 'dict'
schedule_times.desc_short = '''a dictionary of times'''
db.addparamdef(schedule_times,ctxid)
#end parameter: schedule_times

#begin record definition: schedule
schedule = Database.RecordDef()
schedule.name = 'schedule'
schedule.mainview = """$$schedule_times"""
schedule.views['tabularview'] = """$@recname()"""
schedule.views['defaultview'] = """$@recname()"""
schedule.views['recname'] = """$$creator"""
db.addrecorddef(schedule,ctxid)
#end record definition: schedule

#begin parameter: username
username =  Database.ParamDef()
username.name = 'username'
username.vartype = 'string'
username.desc_short = '''username'''
db.addparamdef(username,ctxid)
#end parameter: username

#begin parameter: name_first
name_first =  Database.ParamDef()
name_first.name = 'name_first'
name_first.vartype = 'string'
name_first.desc_short = '''first name'''
db.addparamdef(name_first,ctxid)
#end parameter: name_first

#begin parameter: name_middle
name_middle =  Database.ParamDef()
name_middle.name = 'name_middle'
name_middle.vartype = 'string'
name_middle.desc_short = '''middle name'''
db.addparamdef(name_middle,ctxid)
#end parameter: name_middle

#begin parameter: name_last
name_last =  Database.ParamDef()
name_last.name = 'name_last'
name_last.vartype = 'string'
name_last.desc_short = '''last_name'''
db.addparamdef(name_last,ctxid)
#end parameter: name_last

#begin parameter: email
email =  Database.ParamDef()
email.name = 'email'
email.vartype = 'string'
email.desc_short = '''email'''
db.addparamdef(email,ctxid)
#end parameter: email