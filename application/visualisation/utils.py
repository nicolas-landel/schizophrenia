import math

import plotly.graph_objects as go

# todo table is table_explained_mca
from plotly.offline import offline


def prepare_square_plotly(fs_id1, fs_id2, table):
    """ This function plots a square. It allows us to determine the modalities where the contribution ((weight*(aj)**2))/eigenvalue
    is superior to the weight(nb elements in the modality/ (nb of modalities * nb of features))

    ie : val_abs(ai)<sqrt(eigenvalue i) ie the position of the modality is superior to the square of the eigenvalue of the axe (far enough of the origin)

    """

    # todo refactor
    top_line = go.Scatter(x=[-table.loc[fs_id1, 'Zλ'] ** 0.5, table.loc[fs_id1, 'Zλ'] ** 0.5],
                          y=[table.loc[fs_id2, 'Zλ'] ** 0.5, table.loc[fs_id2, 'Zλ'] ** 0.5],
                          mode='lines',
                          line=go.scatter.Line(color="orange"))

    bottom_line = go.Scatter(x=[-table.loc[fs_id1, 'Zλ'] ** 0.5, table.loc[fs_id1, 'Zλ'] ** 0.5],
                             y=[-table.loc[fs_id2, 'Zλ'] ** 0.5, -table.loc[fs_id2, 'Zλ'] ** 0.5],
                             mode='lines',
                             line=go.scatter.Line(color="orange"))

    right_line = go.Scatter(y=[-table.loc[fs_id2, 'Zλ'] ** 0.5, table.loc[fs_id2, 'Zλ'] ** 0.5],
                            x=[table.loc[fs_id1, 'Zλ'] ** 0.5, table.loc[fs_id1, 'Zλ'] ** 0.5],
                            mode='lines',
                            line=go.scatter.Line(color="orange"))

    left_line = go.Scatter(y=[-table.loc[fs_id2, 'Zλ'] ** 0.5, table.loc[fs_id2, 'Zλ'] ** 0.5],
                           x=[-table.loc[fs_id1, 'Zλ'] ** 0.5, -table.loc[fs_id1, 'Zλ'] ** 0.5],
                           mode='lines',
                           line=go.scatter.Line(color="orange"))

    return [top_line, bottom_line, right_line, left_line]


def interactive_plot_variable_by_variable(table, table_explained_mca, fs_id1, fs_id2, display, square=False,
                                          significant_only=False):
    """
    Categories of the disjunctive data frame in the factor plan. The axis can be modified to chose the factor you want (integer
    between 1 and 10)
    Each variable is represented as a point (using scatter) and they can be removed of the graph in order to focus just on some
    variables

    significant_only is a bool, if false, display all the modalities, if true, only those outside the square (contribution>weight)

    The variables are represented in blue, the label is in red

    Display (bool) : if true, the graph is directly plot, if False, this returns data_ and layout (usefull for the dash)
    The graph is automatically saved as html in the repository current_repository/Images

    """
    # todo table is table_modalities_mca: see what impact
    fs = 'Factor'

    list_name_col_plot = [str(table.columns[i][0]) + ' | ' + str(table.columns[i][1]) for i in
                          range(len(table.columns))]

    data_col = []
    data_lab = []
    coordinates_max = max(max(abs(table.loc[(fs, fs_id1)].values)), max(abs(table.loc[(fs, fs_id2)].values)))

    for i in range(table.shape[1] - 3):
        if significant_only:  # if we plot only the significant modalities ie outside the saquare
            if abs(table.iloc[fs_id1 - 1, i]) > math.sqrt(table_explained_mca.loc[fs_id1, 'Zλ']) and \
                    abs(table.iloc[fs_id2 - 1, i]) > math.sqrt(table_explained_mca.loc[fs_id2, 'Zλ']):
                cols_table = go.Scatter(x=[table.iloc[fs_id1 - 1, i]],
                                        y=[table.iloc[fs_id2 - 1, i]],
                                        hovertext=[list_name_col_plot[i]],
                                        mode='markers',
                                        name='variable {}'.format(list_name_col_plot[i]),
                                        marker=dict(size=10, color="rgba(0,0,255,0.7)"))
                data_col.append(cols_table)

        elif significant_only == False:
            cols_table = go.Scatter(x=[table.iloc[fs_id1 - 1, i]],
                                    y=[table.iloc[fs_id2 - 1, i]],
                                    hovertext=[list_name_col_plot[i]],
                                    mode='markers',
                                    name='variable {}'.format(list_name_col_plot[i]),
                                    marker=dict(size=10, color="rgba(0,0,255,0.7)"))

            data_col.append(cols_table)

    for j in range(1, 4):  # the last columns of the table are label ('aps de risque', 'a risque', 'psychose')
        if j == 1:  # psychose
            color_label = "rgba(255,0,0,0.7)"
        elif j == 2:  # a risque
            color_label = 'rgba(200,180,40,0.9)'
        elif j == 3:  # pas de risque
            color_label = 'rgba(0,220,0,0.7)'
        label_table = go.Scatter(x=[table.iloc[fs_id1 - 1, -j]],
                                 y=[table.iloc[fs_id2 - 1, -j]],
                                 mode='markers',
                                 hovertext=[list_name_col_plot[-j]],
                                 name='{}'.format(list_name_col_plot[-j]),
                                 marker=dict(size=10, color=color_label))

        data_lab.append(label_table)

    data_ = data_col + data_lab

    if square == True:
        data = data_ + prepare_square_plotly(fs_id1, fs_id2)  # if the option 'square limit' is active
        # it will plot a square
    else:
        data = data_

    layout = go.Layout(title="Coordonnées des modalités selon les facteurs " + str(fs_id1) + ' et ' + str(fs_id2),
                       xaxis={"title": "factor" + str(fs_id1),
                              "range": [-coordinates_max - 0.1, coordinates_max + 0.1]},
                       # "gridcolor":"rgba(150,150,150,0.7)", "color":"rgba(100,100,100,0.7)"},
                       yaxis={"title": "factor" + str(fs_id2), "range": [-coordinates_max - 0.1, coordinates_max + 0.1]}
                       # "gridcolor":"rgba(150,150,150,0.7)", "color":"rgba(100,100,100,0.7)"}
                       )

    fig = go.Figure(data=data, layout=layout)

    offline.plot(fig, filename='Images/Variables dans le plan des facteurs scores.html',
                 # to save the figure in the repertory
                 auto_open=False)

    if display:
        offline.iplot(fig)
        return None
    else:
        return data, layout


def interactive_plot_3D_features(fs_id1, fs_id2, fs_id3, table, display=True):  # table is table_modalities_mca
    """
    Plot an interactive graph in 3D  of the modalities
    """

    table_transposed = table.T
    fs = 'Factor'

    list_name_col_plot = [str(table.columns[i][0]) + ' | ' + str(table.columns[i][1]) for i in
                          range(len(table.columns))]

    data_col = []
    data_lab = []
    coordinates_max = max(max(abs(table.loc[(fs, fs_id1)].values)), max(abs(table.loc[(fs, fs_id2)].values))
                          , max(abs(table.loc[(fs, fs_id3)].values)))

    for i in range(table.shape[1] - 3):
        cols_table = go.Scatter3d(x=[table_transposed[('Factor', fs_id1)][i]],
                                  y=[table_transposed[('Factor', fs_id2)][i]],
                                  z=[table_transposed[('Factor', fs_id3)][i]],
                                  hovertext=[list_name_col_plot[i]],
                                  mode='markers',
                                  name='variable {}'.format(list_name_col_plot[i]),
                                  marker=dict(size=10, color="rgba(0,0,255,0.7)"))

        data_col.append(cols_table)

    for j in range(1, 4):  # the last columns of the table are label ('aps de risque', 'a risque', 'psychose')
        if j == 1:  # psychose
            color_label = "rgba(255,0,0,0.7)"
        elif j == 2:  # a risque
            color_label = 'rgba(200,180,40,0.9)'
        elif j == 3:  # pas de risque
            color_label = 'rgba(0,220,0,0.7)'
        label_table = go.Scatter3d(x=[table_transposed[('Factor', fs_id1)][-j]],
                                   y=[table_transposed[('Factor', fs_id2)][-j]],
                                   z=[table_transposed[('Factor', fs_id3)][-j]],
                                   mode='markers',
                                   hovertext=[list_name_col_plot[-j]],
                                   name='{}'.format(list_name_col_plot[-j]),
                                   marker=dict(size=10, color=color_label))

        data_lab.append(label_table)

    data_ = data_col + data_lab

    layout = go.Layout(title="Variables dans le plan 3D des facteurs plans",
                       scene=dict(
                           xaxis={"title": "factor" + str(fs_id1),
                                  "range": [-coordinates_max - 0.1, coordinates_max + 0.1]},
                           yaxis={"title": "factor" + str(fs_id2),
                                  "range": [-coordinates_max - 0.1, coordinates_max + 0.1]},
                           zaxis={"title": "factor" + str(fs_id3),
                                  "range": [-coordinates_max - 0.1, coordinates_max + 0.1]})
                       )

    if display:
        offline.iplot({"data": data_, "layout": layout})
        return None
    else:
        return data_, layout


# Patient graphs


def select_list_to_delete_from_list_to_keep(df, list_to_keep):
    """
    This function is used for the patients' graphs.
    The user select via the application a list of patient to keep (list_to_keep) and this function returns the opposite patients,
    those we want to not plot in the graph. The list will be used to delete the columns in the list ldelete in the
    dataframe table_patients_mca.

    """
    l_delete = []
    for i in range(df.shape[1]):
        if i not in list_to_keep:
            l_delete.append(i)
    return l_delete


def interactive_plot_patient_modality(variable, df_var, table_patients_mca, table_modalities_mca, df_data,
                                      fs_id1=1, fs_id2=2, display=True):
    """
    This function plots the patients into the plan FS_id1, FS_id2 (factors resulting of the MCA)

    The color depends of the value of the feature you selected

    """

    color_ = ['rgba(235,205,40,0.7)', 'rgba(235,0,180,0.7)', 'rgba(0,255,40,0.7)', 'rgba(25,205,40,0.7)',
              'rgba(2,205,150,0.7)', 'rgba(235,105,80,0.7)', 'rgba(150,105,80,0.7)', 'rgba(55,105,180,0.7)',
              'rgba(25,105,230,0.7)', 'rgba(2,105,230,0.7)', 'rgba(5,10,180,0.7)', 'rgba(145,15,180,0.7)',
              'rgba(75,105,180,0.7)', 'rgba(5,105,0,0.7)', 'rgba(5,5,180,0.7)']

    list_color_pat = [0 for i in range(df_var.shape[0])]

    data_ = []  # data for the plot

    # define color for the patients and create data for the features to plot
    for j, modality in enumerate(df_var[variable].columns):
        trace_var = go.Scatter(x=[table_modalities_mca.loc[('Factor', fs_id1), (variable, modality)]],
                               y=[table_modalities_mca.loc[('Factor', fs_id2), (variable, modality)]],
                               hovertext=[variable + ': ' + modality],
                               mode='markers',
                               name=variable + ': ' + modality,
                               marker=dict(size=10, color="rgba(0,0,255,0.7)"))
        data_.append(trace_var)
        for i in range(df_var.shape[0]):
            # if df_var[variable].iloc[i,j]==1:
            if df_var.loc[i, (variable, modality)] == 1:
                list_color_pat[i] = color_[j]

    fs = 'Factor'

    points_x = table_patients_mca.loc[(fs, fs_id1)].values
    points_y = table_patients_mca.loc[(fs, fs_id2)].values
    labels = table_patients_mca.columns.values  # index of patient (1,2,3,...)

    coordinates_max = max(max(abs(table_patients_mca.loc[(fs, fs_id1)].values)),
                          max(abs(table_patients_mca.loc[(fs, fs_id2)].values)))

    # plot the patients
    for i in df_var.index:
        trace = go.Scatter(x=[points_x[i]], y=[points_y[i]], hovertext=str(labels[i]),
                           mode='markers', name='patient {}, valeur :{} '.format(i, df_data.loc[i, variable]),
                           marker=dict(size=10, color=list_color_pat[i]))
        data_.append(trace)

    layout = go.Layout(
        title="Coordonnées des patients projetées dans le plan des facteurs " + str(fs_id1) + ' et ' + str(
            fs_id2) + ' pour la variable ' + variable,
        xaxis={"title": "facteur" + str(fs_id1), "range": [-coordinates_max - 0.1, coordinates_max + 0.1]},
        yaxis={"title": "facteur" + str(fs_id2), "range": [-coordinates_max - 0.1, coordinates_max + 0.1]})

    fig = go.Figure(data=data_, layout=layout)

    offline.plot(fig, filename='Images/Patients dans le plan des facteurs scores.html',
                 # to save the figure in the repertory
                 auto_open=False)

    if display:
        offline.iplot(fig)
        return None
    else:
        return data_, layout


