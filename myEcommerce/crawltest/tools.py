import re
a = "Hello, World!"

url = 'https://shopee.vn/Chu%E1%BB%99t-kh%C3%B4ng-d%C3%A2y-Dareu-LM115G-Black-Pink-B%E1%BA%AET-XA-10M-B%E1%BA%A3o-h%C3%A0nh-24-th%C3%A1ng-ch%C3%ADnh-h%C3%A3ng-i.479108759.11918767540?sp_atk=024f7152-6972-4171-b052-8b42b161ddd3&xptdk=024f7152-6972-4171-b052-8b42b161ddd3'

laz = 'https://www.lazada.vn/products/mqsdl-do-choi-tre-em-2-4cm-24-120-cai-mo-hinh-bup-be-hoat-hinh-pikachu-nhan-vat-nho-nhan-vat-hanh-dong-pokemon-i1358435494-s5613348982.html?&search=pdp_v2v?spm=a2o4n.pdp_revamp.recommendation_2.12.353f7baeSOzSM1&mp=1&scm=1007.16389.286994.0&clickTrackInfo=eb93c8e6-18c1-44a1-bd73-c9ad473383dc__1358435494__10308__trigger2i__287002__0.12__0.12__0.0__0.0__0.0__0.12__11__null__null__null__null__null__null____80000.0__0.4125__4.888888888888889__9__47000.0__129730,138388,138442,138522,138524,138811,141200,141360,141394,141441,141532,141629,141661,141865,142021,148424,148427,154487,154855,154911,160749,168079__null__null__null__3650.16544_955.3632__null__32104__null__0.0__0.0________null__null__0'

product_link = 'https://tiki.vn/do-choi-xuong-rong-nhay-mua-uon-luon-dancing-cactus-phat-ra-am-thanh-vui-nhon-biet-nhai-tieng-p82151219.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_similar-products_UNK_similar-products-v1_202206230600_MD_batched_PID.104270225&itm_medium=CPC&itm_source=tiki-reco&spid=104270225'

sub = url[url.index("-i.")+3:url.index("?")]
sublaz = laz[laz.index("-i")+2:laz.index(".html?")]
product_id = product_link[product_link.index("spid=")+5:]
print(product_id)
