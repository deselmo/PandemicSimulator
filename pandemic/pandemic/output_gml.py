import pandemic as pd
from typing import Sequence


def save_gml(path: str, peers: Sequence[pd.Peer]) -> bool:
    try:
        with open(path, "w") as file:
            file.write(graph(peers))
    except Exception:
        return True

    return False


def print_gml(peers: Sequence[pd.Peer]) -> None:
    print(graph(peers))


def graph(peers: Sequence[pd.Peer]) -> str:
    return(
        'graph ['                                   + '\n' +
        '\t'  + 'directed 1'                        + '\n' +
        ''.join(map(node, peers))                          +
        ''.join(map(edge, peers))                          +
        ']'                                         + '\n'
    )


def node(peer: pd.Peer):
    if peer.data_infection is None:
        return ""

    return(
        '\t' + 'node ['                                      + '\n' +
        '\t' + '\t' + 'id {}'.format(peer.id)                + '\n' +
        '\t' + '\t' + 'label "{}"'.format(node_label(peer))  + '\n' +
        '\t' + ']'                                           + '\n'
    )


def node_label(peer: pd.Peer) -> str:
    return "" if peer.data_patch is None else str(peer.data_patch.epoch)


def edge(peer: pd.Peer) -> str:
    if peer.data_infection is None:
        return ""

    return(
        '\t' + 'edge ['                                                + '\n' +
        '\t' + '\t' + 'source {}'.format(peer.data_infection.source) + '\n' +
        '\t' + '\t' + 'target {}'.format(peer.data_infection.target) + '\n' +
        '\t' + '\t' + 'label "{}"'.format(peer.data_infection.epoch)   + '\n' +
        '\t' + ']'                                                     + '\n'
    )
