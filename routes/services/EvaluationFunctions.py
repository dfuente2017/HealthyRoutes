from math import radians, cos, sin, asin, sqrt
from routes.models import Route


def get_results(threshold_failure = int(), optimal_route = Route(), obtained_route = Route(), validacion = str()):
    intersection_relevant_with_retrieved_nodes = 0
    retrieved_nodes = len(obtained_route.nodes)
    relevant_nodes = len(optimal_route.nodes)

    for obtained_node in obtained_route.nodes:
        for optimal_node in optimal_route.nodes:
            d = get_distance(optimal_node['longitude'], optimal_node['latitude'], obtained_node['longitude'], obtained_node['latitude'])
            #print('Coords optimal: ' + str(optimal_node['longitude']) + ' ' + str(optimal_node['latitude']))
            #print('Coords obtained: ' + str(obtained_node['longitude']) + ' ' + str(obtained_node['latitude']))
            #print('Distancia: ' + str(d))
            if d <= threshold_failure:
                intersection_relevant_with_retrieved_nodes += 1
                #print('break')
                break

    precision = get_precision(intersection_relevant_with_retrieved_nodes, retrieved_nodes)
    recall = get_recall(intersection_relevant_with_retrieved_nodes, relevant_nodes)
    accuracy = get_accuracy(intersection_relevant_with_retrieved_nodes, retrieved_nodes, relevant_nodes)
    fmessure = get_fmessure(precision, recall)

    print(validacion)
    print('Interseccion entre relevantes y recibidos: ' + str(intersection_relevant_with_retrieved_nodes))
    print('Nodos recibidos: ' + str(retrieved_nodes))
    print('Nodos relevantes: ' + str(relevant_nodes))
    print('Precision: ' + str(precision))
    print('Recall: ' + str(recall))
    print('Accuracy: ' + str(accuracy))
    print('Fmessure: ' + str(fmessure))


def get_precision(intersection_relevant_with_retrieved_nodes, retrieved_nodes):
    return intersection_relevant_with_retrieved_nodes/retrieved_nodes


def get_recall(intersection_relevant_with_retrieved_nodes, relevant_nodes):
    return intersection_relevant_with_retrieved_nodes/relevant_nodes


def get_accuracy(intersection_relevant_with_retrieved_nodes, retrieved_nodes, relevant_nodes):
    true_positive = intersection_relevant_with_retrieved_nodes
    false_positives = retrieved_nodes - intersection_relevant_with_retrieved_nodes
    false_negatives = relevant_nodes - intersection_relevant_with_retrieved_nodes

    return ((true_positive)/(true_positive + false_positives + false_negatives))


def get_fmessure(precision, recall):
    return ((precision*recall)/(precision+recall))


def get_distance(lon1 = int(), lat1 = int(), lon2 = int(), lat2 = int()):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c