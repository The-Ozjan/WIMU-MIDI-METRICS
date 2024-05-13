from notebooks.clamp import clamp_wrapper as cw

cw.change_clamp_txt_query("Film music.")
print(cw.clamp_output("text", "music", top_n=5))