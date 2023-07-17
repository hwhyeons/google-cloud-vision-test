
import os


def compare(tuple1,tuple2):
    return tuple1[0] - tuple2[0]

# key_by_start : eps 기준점을 바로 직전으로 할 것인지, 군집의 시작점을 기준으로 할 것인지
def do_cluster(list_xy_text,eps,key_index,key_by_start):
    clusters = []
    points_sorted = sorted(list_xy_text,key=lambda x : x[key_index])
    # points_sorted = sorted(list_x_text,key=lambda x : x[0])

    curr_point = points_sorted[0][key_index]
    curr_cluster = [points_sorted[0]]
    for tp in points_sorted[1:]:
        point = tp[key_index]
        if point <= curr_point + eps:
            curr_cluster.append(tp)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [tp]
            if not key_by_start:
                curr_point = point
        if key_by_start:
            curr_point = point
    clusters.append(curr_cluster)
    return clusters


def detect_text(content):
    """Detects text in the file.가
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    # response = client.text_detection(image=image) 이게 기본 방식
    texts = response.text_annotations
    sum_price = 0 # 전체 금액 합계
    text_list = []
    str_ap = ""
    is_skip = True
    before_x = 0
    product_list= []
    price_list = []
    list_xy_and_text = []
    for text in texts:
        if is_skip:
            is_skip = False
            continue
        # print('\n"{}"'.format(text.description))
        coordinate_list = ['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices]
        vertices = (coordinate_list)
        x_bound = int(vertices[0][1:-1].split(",")[0])
        y_bound = int(vertices[0][1:-1].split(",")[1])
        text_list.append(text.description)
        list_xy_and_text.append((x_bound,y_bound,text.description)) # 형식 : x 시작 좌표 / 문자열

    # 군집화
    clusters_x = do_cluster(list_xy_and_text,40,0,True)  # x축 기준 군집화
    clusters_y = do_cluster(list_xy_and_text,40,1,False)  # y축 기준 군집화

    # 마지막 X축 군집을 금액 군집으로 판정 : 마지막 군집 시작점을 기준으로 분할
    bound_price = clusters_x[-1][0][0]

    # 줄 단위로 분할
    # cluster : 튜플을 포함하는 리스트
    # 하나의 군집 = 한 줄
    for cluster in clusters_y:
        product_name = ""
        for tp in cluster:
            if tp[0] >= bound_price:
                price_list.append(int(str(tp[2]).replace(",", "")))
            else:
                product_name += tp[2]
        product_list.append(product_name)


    print("-----------상품들-----------\n")
    if len(product_list) != len(price_list):
        print("물품명 / 가격 군집화 실패")
        for name in product_list:
            print(name)
        print("-------- 추정 가격 --------")
        for price in price_list:
            print(price)
    else:
        length = len(product_list)
        for i in range(length):
            print(f"상품 : {product_list[i]}  /  가격 : {price_list[i]}")

    print("\n예상 총 금액 : "+str(sum(price_list)))

    file = open("texts_json.json",'w')
    file.write(str(texts))

    text_list = list(map(lambda x: x.description, texts))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return product_list,price_list


if __name__ == '__main__':
    product_list,price_list = detect_text("이미지파일경로")


