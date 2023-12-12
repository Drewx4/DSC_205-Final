

import streamlit as st
#from streamlit_folium import st_folium
#import folium
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.dates import DateFormatter

df2 = pd.read_csv('state_all.csv')

ct_df = pd.read_csv('CT_Performance_Index.csv')

GPA_df = pd.read_csv('school_scores.csv')

ct = df2.loc[df2['STATE'] == 'CONNECTICUT']

st.markdown('---')

st.title("This will be the title, maybe something like 'Student Performance in CT and the US'")
st.write('How has student performance changed in connecticut over time? And how does this compare to other states?')

st.markdown('---')

st.write("Standardized test scores are one measure of student performance. The National Assessment of Educational Progress (NAEP) is a congressionally mandated large-scale assessment administered by the National Center for Education Statistics (NCES). Scores are reported for grades 4 and 8 in key subjects.")

ct_math_4 = ct.dropna(subset='AVG_MATH_4_SCORE').sort_values(by=['YEAR'])
ct_math_8 = ct.dropna(subset='AVG_MATH_8_SCORE').sort_values(by=['YEAR'])
ct_reading_4 = ct.dropna(subset='AVG_READING_4_SCORE').sort_values(by=['YEAR'])
ct_reading_8 = ct.dropna(subset='AVG_READING_8_SCORE').sort_values(by=['YEAR'])

fig = plt.figure()

ax1 = fig.add_subplot(2,2,1)
ax1.bar(ct_math_4['YEAR'].astype(str), ct_math_4['AVG_MATH_4_SCORE'])
ax1.set_ylabel('Average Math Score')
ax1.set_title('Grade 4 Average Math Scores')
ax1.set_ylim(200,300)
ax1.xaxis.set_tick_params(labelsize='xx-small')
ax1.set_xticklabels(ct_math_4['YEAR'], rotation=45, ha='right')

ax2 = fig.add_subplot(2,2,2)
ax2.bar(ct_math_8['YEAR'].astype(str), ct_math_8['AVG_MATH_8_SCORE'])
ax2.set_title('Grade 8 Average Math Scores')
ax2.set_ylim(200,300)
ax2.xaxis.set_tick_params(labelsize='xx-small')
ax2.set_xticklabels(ct_math_8['YEAR'], rotation=45, ha='right')

ax3 = fig.add_subplot(2,2,3)
ax3.bar(ct_reading_4['YEAR'].astype(str), ct_reading_4['AVG_READING_4_SCORE'])
ax3.set_xlabel('Year')
ax3.set_ylabel('Average Reading Score')
ax3.set_title('Grade 4 Average Reading Scores')
ax3.set_ylim(200,300)
ax3.xaxis.set_tick_params(labelsize='xx-small')
ax3.set_xticklabels(ct_reading_4['YEAR'], rotation=45, ha='right')

ax4 = fig.add_subplot(2,2,4)
ax4.bar(ct_reading_8['YEAR'].astype(str), ct_reading_8['AVG_READING_8_SCORE'])
ax4.set_xlabel('Year')
ax4.set_title('Grade 8 Average Reading Scores')
ax4.set_ylim(200,300)
ax4.xaxis.set_tick_params(labelsize='xx-small')
ax4.set_xticklabels(ct_reading_8['YEAR'], rotation=45, ha='right')

fig.tight_layout(h_pad=2)

st.subheader('\nAverage NAEP Test Scores for CT')

container1 = st.container(border=True)
if container1.checkbox('Show figure', value=True):
    st.pyplot(fig = fig)

st.markdown('---')

st.subheader('Student Performance Indices in CT over Time')
st.write("Performance indices are another way schools measure performance of students in a subject area (i.e., ELA, Mathematics or Science) on state summative assessments. The Performance Index ranges from 0-100 and is reported for all students, and for students in each individual student group. Connecticut's ultimate goal for these indices is 75.")

#Grab PI for all students, replace NaN's with 0, reset index next block
all_students = ct_df.loc[ct_df['Category'] == 'All Students']
all_students.replace(np.nan, 0)

#Missing data during pandemic years, add two rows of zeros and change school year to gap years
all_students = all_students.append(pd.Series(0, index=all_students.columns), ignore_index=True)
all_students = all_students.append(pd.Series(0, index=all_students.columns), ignore_index=True)
all_students['School Year'][7] = '2019-2020'
all_students['School Year'][8] = '2020-2021'
all_students = all_students.reset_index(drop=True)



#Change performance index to floats and school year to strings
all_students['ELAPerformanceIndex'] = all_students['ELAPerformanceIndex'].astype(float)
all_students['MathPerformanceIndex'] = all_students['MathPerformanceIndex'].astype(float)
all_students['SciencePerformanceIndex'] = all_students['SciencePerformanceIndex'].astype(float)

all_students['School Year'] = all_students['School Year'].astype(str)

all_students = all_students.sort_values(by=['School Year'])

#Figure and subplots
ct_per = plt.figure()
ct_per.suptitle('CT Performance Indices from 2014 to 2023 for Key Subjects')

ax1 = ct_per.add_subplot(2,2,1)

ax1.bar(all_students['School Year'], all_students['ELAPerformanceIndex'])
ax1.set_xlabel('School Year')
ax1.set_ylabel('Performance Index')
ax1.set_title('ELA Performance')
ax1.set_ylim(0,100)
ax1.xaxis.set_tick_params(labelsize='xx-small')
ax1.set_xticklabels(all_students['School Year'], rotation=45, ha='right')

ax2 = ct_per.add_subplot(2,2,2)

ax2.bar(all_students['School Year'], all_students['MathPerformanceIndex'])
ax2.set_xlabel('School Year')
ax2.set_ylabel('Performance Index')
ax2.set_title('Math Performance')
ax2.set_ylim(0,100)
ax2.xaxis.set_tick_params(labelsize='xx-small')
ax2.set_xticklabels(all_students['School Year'], rotation=45, ha='right')

ax3 = ct_per.add_subplot(2,2,3)

ax3.bar(all_students['School Year'], all_students['MathPerformanceIndex'])
ax3.set_xlabel('School Year')
ax3.set_ylabel('Performance Index')
ax3.set_title('Science Performance')
ax3.set_ylim(0,100)
ax3.xaxis.set_tick_params(labelsize='xx-small')
ax3.set_xticklabels(all_students['School Year'], rotation=45, ha='right')

ct_per.tight_layout(h_pad=2)

st.pyplot(fig=ct_per)


st.markdown('---')

st.markdown('---')

st.subheader('How do CT scores compare to other states?')

st.markdown('---')



container = st.container(border=True)
c1,c2,c3 = container.columns(3)

state_input0 = c1.selectbox('Select a state: ', ['Alabama', 'Alaska', 'Arizona',
  'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
  'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
  'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
  'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
  'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
  'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
  'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'], placeholder='Mississippi')

subject_input = c2.radio('Select a subject: ', ['Reading', 'Math'])

grade_input = c3.radio('Select a grade level: ', ['4','8'])

state_input = '_'.join(state_input0.split(' ')).upper()

state_df = df2.loc[df2['STATE'] == state_input].reset_index()

state_name = state_df['STATE'][0]

fig2 = plt.figure()

fig2.suptitle(state_input0 + ' vs Connecticut')

subset_select = 'AVG_' + subject_input.upper() + '_' + grade_input + '_SCORE'
data_select = state_df.dropna(subset=subset_select).sort_values(by=['YEAR']).reset_index()

s_title = 'Grade ' + grade_input + ' Average ' + subject_input + ' Scores'
ylab = 'Average ' + subject_input + ' Score'

if grade_input == '4':
  upper_lim = 260
else:
  upper_lim = 300

ax_st = fig2.add_subplot(1,2,1)
ax_st.bar(data_select['YEAR'].astype(str), data_select[subset_select])
ax_st.set_ylabel(ylab)
ax_st.set_xlabel('Year')
ax_st.set_title(s_title)
ax_st.set_ylim(200,upper_lim)
ax_st.xaxis.set_tick_params(labelsize='xx-small')
ax_st.set_xticklabels(data_select['YEAR'], rotation=45, ha='right')

ct_select = ct.dropna(subset=subset_select).sort_values(by=['YEAR'])

ax_ct = fig2.add_subplot(1,2,2)
ax_ct.bar(ct_select['YEAR'].astype(str), ct_select[subset_select])
#ax_ct.set_ylabel(ylab)
ax_ct.set_xlabel('Year')
ax_ct.set_title(s_title)
ax_ct.set_ylim(200,upper_lim)
ax_ct.xaxis.set_tick_params(labelsize='xx-small')
ax_ct.set_xticklabels(ct_select['YEAR'], rotation=45, ha='right')

fig2.tight_layout(h_pad=2)

st.pyplot(fig=fig2)

st.markdown('---')

container3 = st.container(border=True)
c4,c5 = container3.columns(2)

subject_input1 = c4.selectbox('Select subject one:', ['Arts/Music', 'English', 'Foreign Languages', 'Mathematics', 'Natural Sciences', 'Social Sciences/History'])
subject_input2 = c5.selectbox('Select subject two:', ['Arts/Music', 'English', 'Foreign Languages', 'Mathematics', 'Natural Sciences', 'Social Sciences/History'])

GPA_dist = plt.figure()

ax = GPA_dist.add_subplot()

col1 = str('Academic Subjects.' + ' '.join(subject_input1.split(' ')) + '.Average GPA')
col2 = str('Academic Subjects.' + ' '.join(subject_input2.split(' ')) + '.Average GPA')

ax.hist(GPA_df[col1].astype(float), bins = 50, alpha=0.75, label = subject_input1)
ax.hist(GPA_df[col2].astype(float), bins = 50, alpha=0.5, label = subject_input2)

ax.set_xlabel('GPA')
ax.set_ylabel('Frequency')
ax.set_title('GPA Distributions for ' + subject_input1 + ' and ' + subject_input2 + ' Among US States and Territories')

ax.legend()

GPA_dist.text(.6, 0, 'Data displayed is from 2005 to 2015', bbox = dict(facecolor = 'gray', alpha = 0.5))

st.pyplot(fig=GPA_dist)

st.markdown('---')

st.markdown('---')

container2 = st.container(border=True)

year_choice = container2.slider('Select a year:', 2005, 2015)
subject_input3 = container2.selectbox('Select a subject:', ['Arts/Music', 'English', 'Foreign Languages', 'Mathematics', 'Natural Sciences', 'Social Sciences/History'])

col3 = str('Academic Subjects.' + ' '.join(subject_input3.split(' ')) + '.Average GPA')

GPA_year = GPA_df.loc[GPA_df['Year'] == int(year_choice)]

state_map = folium.Map(location=(40,-96), zoom_start=4, scrollWheelZoom=False, dragging=False)
state_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
state_bounds = f"{state_url}/us-states.json"

choro = folium.Choropleth(
          geo_data=state_bounds,
          name="choropleth",
          data = GPA_year,
          columns = ['State.Code', col3],
          key_on="feature.id",
          fill_color= 'PuBu',
          fill_opacity=0.7,
          line_opacity=0.2,
          legend_name="GPA"
          )
choro.add_to(state_map)

st_folium(state_map, width = 725)


st.markdown('---')
