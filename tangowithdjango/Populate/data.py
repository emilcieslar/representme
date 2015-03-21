from dateutil import parser
from tangowithdjango import settings
import os
__author__ = '2168879m'
"""
This file contains all the static information accessed by populating function definitions
I strongly encourage you to put any other such information here to make it:
    - easy to view out-dated info
    - easy to change
    - accessible by other functions
"""

# topics for divisions
topics = {
'unknown':'',                                  #0
'Agriculture':'',                              #1
'Civil and Criminal Justice':'',               #2
'Education':'',                                #3
'Environment':'',                              #4
'Health':'',                                   #5
'Housing':'',                                  #6
'Local Government':'',                         #7
'Planning/Future':'',                          #8
'Police and Fire Services':'',                 #9
'Social Work':'',                              #10
'Sports and the Arts':'',                      #11
'Transport':''                                 #12
}

# change the topic_extracter location script here
topic_extracter_location = 'scraper.report_scraper'
topic_extracter_name = '.topic_extracter'

# change here the number of msps
number_of_msps = 128

# change here for location of scraped divisions
divisions_location = os.path.join(settings.PROJECT_PATH, 'tangowithdjango', 'scraper', 'report_scraper', 'new_data')

# change here to only get subset of divisions
startdate = '02 June 2011'          # first meeting of new parliament       -- 2 June 2011
enddate = '6 May 2016'              # last day of new parliament            -- 6 May 2016

# add here independent parties:
independent_parties = [
    'No Party Affiliation',
    'Independent'
]

string1 = 'The Scottish National Party (SNP) is the main political party in Scotland which supports Scotland becoming ' \
          'an independent nation. They are overall centre-left, advocating social democracy, nuclear disarmament and ' \
          'closer ties to the European Union. \n They were founded in 1934 and formed a permanent grouping in parliament ' \
          'in 1967. Their best election result in the 20th century was at the general election of October 1974 in which ' \
          'they won 11 of Scotland\'s 72 Westminster seats as well as around 30% of the popular vote, however they lost ' \
          'all but 2 of these seats in 1979. Support for the party was bolstered under the leadership of Alex Salmond, ' \
          'who in 2011 led the SNP to their best electoral performance to date, in which they became the first party in ' \
          'the devolved Scottish Parliament to win a majority of seats. \n They currently form the Scottish government, ' \
          'and are now led by Scotland\'s First Minister, Nicola Sturgeon. They currently have 61 MSPs, 6 MPs and 2 MEPs.'.encode('latin1','ignore')
string2 = 'The Scottish Labour Party was the most successful party in Scottish elections from 1959 to 2007. ' \
          'Like the wider UK Labour Party, they are centre-left and they promote British unionism. \n' \
          'They first overtook the Conservatives as Scotland\'s largest party at the 1959 general election. ' \
          'In 1997, the UK Labour Party under Tony Blair offered Scotland a referendum on devolution ' \
          'which was passed with around 74% of the electorate in favour. From 1999 to 2007, they were in power ' \
          'in the Scottish Parliament through a coalition with the Liberal Democrats. From 2008-2011, ' \
          'the party was led by Iain Gray in the Scottish Parliament, who announced his resignation ' \
          'after the party\'s defeat at the 2011 Scottish election. Johann Lamont became leader in 2011 ' \
          'and resigned in 2014 after an internal dispute within the party. \n They currently control 40/59 ' \
          'Scottish seats in the House of Commons. They also have 37 seats in the Scottish Parliament and have 2 MEPs.'.encode('latin1','ignore')
string3 = 'The Scottish Conservative and Unionist Party was founded in 1965 out of the old Scottish Unionist Party, ' \
          'which had been a dominant political force in Scotland for much of the early 20th century, winning ' \
          'the majority of votes and seats in the 1955 general election. \n However the party went into decline, ' \
          'being reduced from 21 Scottish seats in 1983, to 10 in 1987. The 1997 general election was a catastrophe ' \
          'for the Scottish Conservatives, who were left with no Scottish seats whatsoever. However the party ' \
          'won 18 seats in the Scottish Parliament in the 1999 election due to proportional representation. ' \
          'Since 2001 the Conservatives have held 1 Scottish seat in the UK parliament. \n Like the wider ' \
          'UK Conservative Party, the party is a centre-right party, which promotes conservatism and British unionism. \n' \
          'They are currently have 15 MSPs, led in the Scottish Parliament by Ruth Davidson, 1 MP and 1 MEP.'.encode('latin1','ignore')
string4 = 'An independent or nonpartisan politician is an individual politician not affiliated to any political party. \n\n' \
          'Independents may hold a centrist viewpoint between those of major political parties. ' \
          'Sometimes they hold a viewpoint more extreme than any major party, have an ideology comprising ideas ' \
          'from both sides of the political spectrum, or may have a viewpoint based on issues that they do not feel ' \
          'that any major party addresses. \n Other independent politicians may be associated with a political party, ' \
          'be former members of it, or have views that align with it, but choose not to stand under its label. ' \
          'Others may belong to or support a political party but believe they should not formally represent it and ' \
          'thus be subject to its policies.'.encode('latin1','ignore')
string5 = 'The Scottish Green Party is centre-left and promotes Scottish independence and environmentalism. ' \
          'It retains close ties with the Green Party of England and Wales, both having originated in ' \
          'the breakup of the UK Green Party. \n It won a seat in the Scottish Parliament in 1999, which was ' \
          'increased to 7 in 2003, and then reduced to 2 in 2007. The Greens retained both these seats in 2011.'.encode('latin1','ignore')
string6 = 'The Scottish Liberal Democrats are a centre to centre-left social liberal party. They were formed out of ' \
          'the old Liberal Party and the Social Democratic Party in 1988. \n Currently, they are Scotland\'s second ' \
          'largest party in terms of seats in the UK Parliament, controlling 11 out of 59. Their leader is Willie Rennie. ' \
          'Since the formation of the Conservative-Liberal Democrat coalition at Westminster, support for ' \
          'the Liberal Democrats has fallen sharply, and the party won only 5 seats at the 2011 Scottish ' \
          'parliamentary election. They also lost their Scottish MEP at the 2014 European Elections.'.encode('latin1','ignore')
string7 = 'The Presiding Officer is expected to be nonpartisan. For this reason, it is customary for the Presiding Officer ' \
          'to suspend his or her party membership for the duration of his or her term.'.encode('latin1','ignore')
# links and descriptions for parties
# descriptions from wikipedia
party_links_colours = {
'Scottish National Party'                   : ('http://www.snp.org/', string1,
                                               'http://en.wikipedia.org/wiki/List_of_political_parties_in_Scotland#Political_parties',
                                                '#F6DC60'),
'Scottish Labour'                           : ('http://www.scottishlabour.org.uk/', string2,
                                               'http://en.wikipedia.org/wiki/List_of_political_parties_in_Scotland#Political_parties',
                                                '#EB2743'),
'Scottish Conservative and Unionist Party'  : ('http://www.scottishconservatives.com/', string3,
                                               'http://en.wikipedia.org/wiki/List_of_political_parties_in_Scotland#Political_parties',
                                                '#5ABFF4'),
'Independent'                               : ('', string4,
                                               'http://en.wikipedia.org/wiki/Independent_politician',
                                                '#986561'),
'Scottish Green Party'                      : ('http://www.scottishgreens.org.uk/', string5,
                                               'http://en.wikipedia.org/wiki/List_of_political_parties_in_Scotland#Political_parties',
                                                '#31C48E'),
'Scottish Liberal Democrats'                : ('http://www.scotlibdems.org.uk/', string6,
                                               'http://en.wikipedia.org/wiki/List_of_political_parties_in_Scotland#Political_parties',
                                                '#FF6936'),
'No Party Affiliation'                      : ('', string7,
                                               'http://en.wikipedia.org/wiki/Presiding_Officer_of_the_Scottish_Parliament',
                                                '#475070'),
}

# Group decided not to keep them, cause you cannot follow anymore
# msps for the current session that were not members at the time of scraping
'''
former_or_new_msps = [
('Aberdeen Donside',
 'Scottish National Party',
 MSP(firstname='Brian', lastname='Adam',
     member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse(' 25 April 2013'),
     party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('25 April 2013'),
     status=MSP.DECEASED, foreignid=129,)),
('Cowdenbeath',
 'Scottish Labour',
 MSP(firstname='Helen', lastname='Eadie',
     member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse('9 November 2013'),
     party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('9 November 2013'),
     status=MSP.DECEASED, foreignid=130)),
('Lothian',
 'Independent',
 MSP(firstname='Margo', lastname='MacDonald',
     member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('4 April 2014'),
     party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('4 April 2014'),
     status=MSP.DECEASED, foreignid=131)),
('Lothian',
 'Scottish Conservative and Unionist Party',
 MSP(firstname='David', lastname='McLetchie',
     member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('12 August 2013'),
     party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('12 August 2013'),
     status=MSP.DECEASED, foreignid=132)),
('Mid Scotland and Fife',
 'Scottish Labour',
 MSP(firstname='John', lastname='Park',
     member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('9 November 2012'),
     party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('7 September 2013'),
     status=MSP.RESIGNED, foreignid=133)),
('Dunfermline',
 'Independent',
 MSP(firstname='Bill', lastname='Walker',
     member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse(' 9 September 2013'),
     party_startdate = parser.parse('3 March 2012'), party_enddate = parser.parse(' 9 September 2013'),
     status=MSP.RESIGNED, foreignid=134))
]
'''

# cabinet here http://en.wikipedia.org/wiki/Scottish_Government#Ministers
# positions held by msps during the current parliament session
positions = [
['Brian','Adam','Minister for Parliamentary Business and Chief Whip',parser.parse('25 May 2011'),parser.parse('6 September 2012')],
['Alasdair', 'Allan', 'Minister for Learning, Science and Scotland\'s Languages', parser.parse('7 December 2011'),parser.parse('5 May 2016')],
['Claire','Baker','Deputy Convener of the Scottish Parliament Education and Culture Committee',parser.parse('14 June 2011'), parser.parse('5 May 2016')],
['Marco','Biagi','Minister for Local Government and Community Empowerment',parser.parse('5 May 2011'),parser.parse('5 May 2016')],
['Gavin','Brown','Convener of the Scottish Parliament Economy, Energy and Tourism Committee',parser.parse('8 June 2011'),parser.parse('5 May 2016')],
['Keith','Brown','Cabinet Secretary for Infrastructure, Investment and Cities',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Keith','Brown','Minister for Transport and Veterans',parser.parse('11 December 2010'),parser.parse('21 November 2014')],
['Margaret','Burgess','Minister for Housing and Welfare',parser.parse('5 September 2012'),parser.parse('5 May 2016')],
['Aileen','Campbell','Minister for Children and Young People',parser.parse('7 December 2011'),parser.parse('5 May 2016')],
['Aileen','Campbell','Minister for Local Government and Planning',parser.parse('25 May 2011'),parser.parse('7 December 2011')],
['Jackson','Carlaw','Deputy Leader of the Scottish Conservatives',parser.parse('10 November 2011'),parser.parse('5 May 2016')],
['Angela', 'Constance', 'Minister for Youth Employment', parser.parse('7 December 2011'),parser.parse('22 April 2014')],
['Angela', 'Constance', 'Cabinet Secretary for Education and Lifelong Learning', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Angela', 'Constance', 'Cabinet Secretary for Training, Youth and Women\'s Employment', parser.parse('22 April 2014'),parser.parse('21 November 2014')],
['Angela', 'Constance', 'Minister for Children and Young People', parser.parse('25 May 2011'),parser.parse('7 December 2011')],
['Angela', 'Constance', 'Minister for Skills and Lifelong Learning', parser.parse('12 December 2010'),parser.parse('25 May 2011')],
['Bruce','Crawford','Cabinet Secretary for Parliament and Government Strategy',parser.parse('19 May 2011'),parser.parse('5 September 2012')],
['Roseanna','Cunningham','Cabinet Secretary for Fair Work, Skills and Training',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Roseanna','Cunningham','Minister for Community Safety and Legal Affairs',parser.parse('25 May 2011'),parser.parse('21 November 2014')],
['Ruth','Davidson','Leader of the Scottish Conservatives',parser.parse('4 November 2011'),parser.parse('5 May 2016')],
['Nigel','Don','Convener of the Scottish Parliament Subordinate Legislation Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Bob','Doris','Deputy Convener of the Scottish Parliament Health and Sport Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['James','Dornan','Deputy Convener of the Scottish Parliament Subordinate Legislation Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Helen','Eadie','Deputy Convener of the Scottish Parliament Standards, Procedures and Public Appointments Committee',parser.parse('14 June 2011 '),parser.parse('9 November 2013')],
['Annabelle','Ewing','Deputy Convener of the Scottish Parliament Rural Affairs, Climate Change and Environment Committee',parser.parse('15 June 2011'),parser.parse('21 November 2014')],
['Fergus','Ewing','Minister for Energy, Enterprise and Tourism',parser.parse('20 May 2011'), parser.parse('5 May 2016')],
['Linda','Fabiani','Convener of the Scottish Parliament Scotland Bill Committee',parser.parse('21 June 2011'),parser.parse('5 May 2016')],
['Mary','Fee','Convener of the Scottish Parliament Equal Opportunities Committee',parser.parse('10 January 2012'),parser.parse('5 May 2016')],
['Joe','FitzPatrick','Minister for Parliamentary business',parser.parse('5 September 2012'),parser.parse('5 May 2016')],
['Murdo','Fraser','Deputy Convener of the Scottish Parliament Public Audit Committee',parser.parse('20 June 2007'),parser.parse('5 May 2016')],
['Kenneth','Gibson','Convener of the Scottish Parliament Finance Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Rob','Gibson','Convener of the Scottish Parliament Rural Affairs, Environment and Climate Change Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Christine','Grahame','Convener of the Scottish Parliament Justice Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Hugh','Henry','Convener of the Scottish Parliament Public Audit Committee',parser.parse('26 September 2007'),parser.parse('5 May 2016')],
['Jamie','Hepburn','Minister for Sport and Health Improvement',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Fiona','Hyslop','Cabinet Secretary for Culture, Europe and External Affairs',parser.parse(''),parser.parse('5 May 2016')],
['James','Kelly','Shadow Cabinet Secretary for Infrastructure, Investment and Cities Strategy',parser.parse('28 June 2013'),parser.parse('5 May 2016')],
['James','Kelly','Labour Chief Whip',parser.parse('10 January 2012'),parser.parse('28 June 2013')],
['James','Kelly','Deputy Convener of the Scottish Parliament Scotland Bill Committee',parser.parse('21 June 2011'),parser.parse('5 May 2016')],
['James','Kelly','Deputy Convener of the Scottish Parliament Justice Committee',parser.parse('14 June 2011'),parser.parse('10 January 2012')],
['Johann','Lamont','Leader of the Scottish Labour Party',parser.parse('17 December 2011'),parser.parse('24 October 2014')],
['Richard','Lochhead','Cabinet Secretary for Rural Affairs, Food and Environment',parser.parse('17 May 2007'),parser.parse('5 May 2016')],
['Kenny','MacAskill','Cabinet Secretary for Justice',parser.parse('17 May 2007'),parser.parse('21 November 2014')],
['Derek','Mackay','Minister for Transport and Islands',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Derek','Mackay','Minister for Local Government and Planning',parser.parse('7 December 2011'),parser.parse(' 21 November 2014')],
['Hanzala','Malik','Deputy Convener of the Scottish Parliament European and External Relations Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Tricia','Marwick','4th Presiding Officer of the Scottish Parliament',parser.parse('11 May 2011'),parser.parse('5 May 2016')],
['John','Mason','Deputy Convener of the Scottish Parliament Finance Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Michael','Matheson','Cabinet Secretary for Justice',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Michael','Matheson','Minister for Public Health',parser.parse('20 May 2011'),parser.parse('21 November 2014')],
['Stewart','Maxwell','Convener of the Scottish Parliament Education and Culture Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Joan','McAlpine','Parliamentary Liaison Officer to the First Minister of Scotland',parser.parse('5 May 2011'),parser.parse('5 May 2016')],
['Christina','McKelvie','Convener of the Scottish Parliament European and External Relations Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Duncan','McNeil','Convener of the Scottish Parliament Health and Sport Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Alex','Neil','Cabinet Secretary for Social Justice, Communities and Pensioners\' Rights',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Alex','Neil','Cabinet Secretary for Health and Wellbeing',parser.parse('5 September 2012'),parser.parse('21 November 2014')],
['Willie','Rennie','Leader of the Scottish Liberal Democrats',parser.parse('17 May 2011'),parser.parse('5 May 2016')],
['Shona','Robison','Cabinet Secretary for Health, Wellbeing and Sport',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Shona','Robison','Cabinet Secretary for Commonwealth Games, Sport, Equalities and Pensioners\ Rights',parser.parse('22 April 2014'),parser.parse('1 November 2014')],
['Michael','Russell','Cabinet Secretary for Education and Lifelong Learning',parser.parse('1 December 2009'),parser.parse('21 November 2014')],
['Alex', 'Salmond', 'First Minister', parser.parse('16 May 2007'), parser.parse('20 November 2014')],
['Alex', 'Salmond', 'Leader of the Scottish National Party', parser.parse('3 September 2004'), parser.parse('14 November 2014')],
['John', 'Scott', 'Deputy Presiding Officer', parser.parse('11 May 2011'), parser.parse('5 May 2016')],
['Elaine', 'Smith', 'Deputy Presiding Officer', parser.parse('11 May 2011'), parser.parse('5 May 2016')],
['Stewart','Stevenson','Minister for Environment and Climate Change',parser.parse('25 May 2011 '),parser.parse('6 September 2012')],
['David','Stewart','Convener of the Scottish Parliament Public Petitions Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Kevin','Stewart','Convener of the Scottish Parliament Local Government and Regeneration Committee',parser.parse('1 November 2012'),parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'First Minister', parser.parse('20 November 2014'), parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'Leader of the Scottish National Party', parser.parse('14 November 2014'), parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'Deputy First Minister of Scotland', parser.parse('17 May 2007'), parser.parse(' 19 November 201')],
['Nicola', 'Sturgeon', 'Cabinet Secretary for Infrastructure, Investment and Cities', parser.parse('5 September 2012'), parser.parse('19 November 2014')],
['John', 'Swinney', 'Cabinet Secretary for Finance, Constitution and Economy', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['John', 'Swinney', 'Deputy First Minister of Scotland', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['John', 'Swinney', 'Cabinet Secretary for Finance, Constitution and Economy', parser.parse('17 May 2007'),parser.parse('5 May 2016')],
['Dave','Thompson','Convener of the Scottish Parliament Standards, Procedures and Public Appointments Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Maureen','Watt','Minister for Public Health',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Maureen','Watt','Minister for Public Health',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Maureen','Watt','Convener of the Scottish Parliament Infrastructure and Capital Investment Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Sandra','White','Deputy Convener of the Scottish Parliament Public Petitions Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['John','Wilson','Deputy Convener of the Scottish Parliament Economy, Energy and Tourism Committee',parser.parse('8 June 201'),parser.parse('5 May 2016')],
['Humza','Yousaf','Minister for Europe and International Development',parser.parse('6 September 2012'),parser.parse('5 May 2016')],
['Humza','Yousaf','Parliamentary Liaison Officer to the First Minister of Scotland',parser.parse('6 May 2011 '),parser.parse('6 September 2012')]
]
