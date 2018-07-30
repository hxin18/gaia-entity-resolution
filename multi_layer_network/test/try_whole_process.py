import sys
sys.path.append("..")
import  src.AIF_RPI_to_JSON as rtj
import src.links_edge_list_with_nil as lel
import src.connected_components as cn
input_file = "../data/RPI_clusters_seedling.nt"
output_file = "../data_out/RPI_clusters_seedling_cluster_heads2.json"
output_file2 = "../data_out/RPI_clusters_seedling_same_link_with_nil_d2.edgelist"
#rtj.extract_canonical_mentions_as_cluster_heads(input_file,output_file)
lel.get_links_edge_list(output_file,output_file2)
#cn.main(0)