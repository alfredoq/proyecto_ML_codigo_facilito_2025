def filter_df_based_on_cutoff(df, cutoff, templates_path='./files'):
    filter_pdb_file = f"{templates_path}/{cutoff}A-selection.pdb"
    columns_filter = filter_df_based_on_pdb_file(filter_pdb_file)
    
    filtered_cols = [col for col in df.columns if any(s in col for s in columns_filter)]
    filtered_df = df[filtered_cols]
                
    return filtered_df

def filter_df_based_on_pdb_file(pdb_file, templates_path='../files'):
    with open(pdb_file,'r') as file:
        columns_prefix_filters = []
        for line in file:
            line_split = line.rsplit()
            if len(line_split) > 1:
                if line_split[0] == "ATOM":
                    resname = line_split[3]
                    resnumber = line_split[5]
                    colname_prefix = resname + resnumber
                    if colname_prefix not in columns_prefix_filters:
                        columns_prefix_filters.append(colname_prefix)

    file.close()
    ## append the strings values in the dataframe to the list
    columns_prefix_filters.extend(["assay_id","ligname","sub_pose","binder"])

    
    return columns_prefix_filters

def show_subpose_interactions(filtered_df_clean, interactions_list, sub_poses_list, true_label, predicted_label):
    interactions_list.insert(0, "sub_pose")
    interactions_list.insert(0, "assay_id")
    subseted_df = filtered_df_clean[interactions_list]
    subseted_df_subpose = subseted_df[subseted_df["sub_pose"].isin(sub_poses_list)]
    subseted_df_subpose["True_label"] = true_label
    subseted_df_subpose["Predicted_label"] = predicted_label

    return subseted_df_subpose