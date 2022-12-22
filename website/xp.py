"""Main OpenClassRooms scrapping."""

import os
import sys

# from pathlib import Path
from pprint import pprint

import logging

import networkx as nx
import matplotlib.pyplot as plt

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from .ocr import OpenClassrooms

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

# from project.settings import zenvar
# from zutils import zmongodb as db_client


# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)


def show_menu():
    """Show menu."""

    print("Choices:")
    print("Operations:")
    print("[U]pdate content(s)")
    print("[T] Update dependecies")
    print("[S]how content(s)")
    print("[F]ilter content(s)")
    print("[G] Draw Content network graph")
    print("[C] Dependency Sanity Check")
    print("[M] Minimize Dependency")
    print("[Q]uit")
    print("delete series")
    print("Drop database")


def execute_operation(operation_id):

    if operation_id == "u":
        update_content()
    elif operation_id == "t":
        update_course_dependency()
    elif operation_id == "s":
        show_content()
    elif operation_id == "f":
        filter_content()
    elif operation_id == "g":
        graph_content()
    elif operation_id == "c":
        check_dependency_sanity()
    elif operation_id == "m":
        minimize_dependency()


def update_content():

    ocr_obj = OpenClassrooms()
    ocr_obj.get_posts(page_start_idx=4, n_page_max=0)
    content_lst = ocr_obj.post_lst

    if content_lst:

        # logger.debug(content_lst)
        db = __get_db()
        for content_idx, content_dct in enumerate(content_lst):

            cursor = db.inventory.find({"identifier": content_dct["identifier"]})

            # delete duplicated
            duplicated_lst = [item_dct for item_dct in cursor]
            if duplicated_lst:
                duplicated_lst.pop(0)

            for item_dct in duplicated_lst:
                del_res = db.inventory.delete_one(item_dct)
                print(
                    "Delete: ",
                    item_dct["title"],
                    del_res.acknowledged,
                    del_res.deleted_count,
                    del_res.raw_result,
                )

            # update origin
            update_res = db.inventory.update_one(
                {"identifier": content_dct["identifier"]},
                {"$set": content_dct, "$currentDate": {"lastModified": True}},
            )
            update_res_s = (
                f"{content_idx}. Update: {update_res.acknowledged}, "
                f'{content_dct["identifier"]} {content_dct["label"]}, '
                f"Found: {update_res.matched_count}, "
                f"Updated: {update_res.modified_count}, Raw: {update_res.raw_result}, "
                f"U: {update_res.upserted_id}"
            )

            if update_res.matched_count > 1:
                logger.error(f"Duplicated document: {update_res_s}")
            if update_res.matched_count == 1:
                logger.debug(update_res_s)
            else:
                insert_res = db.inventory.insert_one(content_dct)
                logger.debug(
                    f"""{content_idx}. Insert: {insert_res.acknowledged}, {insert_res.inserted_id} - {content_dct['identifier']} {content_dct['label']}"""
                )


def update_course_dependency():

    db = __get_db()

    cursor = db.inventory.find({"type": "course"})
    content_id_lst = [document["identifier"] for document in cursor]

    with WebDriver() as driver:

        for content_idx, content_id in enumerate(content_id_lst):

            cursor = db.inventory.find({"identifier": content_id})
            if cursor:

                content_dct = cursor[0]

                if "dependency_lst" not in content_dct:

                    content_url = content_dct["url"]
                    dependency_dct = ocr.import_source_content_dependency(
                        driver, content_url
                    )

                    title = content_dct["title"]

                    dependency_lst = [
                        {"identifier": dependency[0], "label": dependency[1]}
                        for idx, dependency in enumerate(
                            dependency_dct["dependency_lst"]
                        )
                    ]

                    if dependency_lst:

                        update_res = db.inventory.update_one(
                            {"identifier": content_dct["identifier"]},
                            {
                                "$set": {"dependency_lst": dependency_lst},
                                "$currentDate": {"lastModified": True},
                            },
                        )
                        logger.debug(
                            "{}. Update: {}, {}, {}, {}, {}, {}, {}".format(
                                content_idx,
                                content_dct["identifier"],
                                title,
                                update_res.acknowledged,
                                update_res.matched_count,
                                update_res.modified_count,
                                update_res.raw_result,
                                update_res.upserted_id,
                            )
                        )

                    else:
                        logger.debug(
                            "{}. No Dependency Found for ID: {}".format(
                                content_idx,
                                content_id,
                            )
                        )

            else:
                logger.error(
                    "{}. Update: {}, {}, {}, {}, {}, {}, {}".format(
                        content_idx,
                        content_dct["identifier"],
                        title,
                        update_res.acknowledged,
                        update_res.matched_count,
                        update_res.modified_count,
                        update_res.raw_result,
                        update_res.upserted_id,
                    )
                )


def show_content():

    db = __get_db()
    cursor = db.inventory.find({})

    for inventory in cursor:
        pprint(inventory, indent=4, compact=True)


def filter_content():

    db = __get_db()
    cursor = db.inventory.find({"type": "path", "category": "DATA"})

    for idx, inventory in enumerate(cursor):
        pprint("{} - {}".format(idx, inventory), indent=4, compact=True)

    cursor = db.inventory.find({"type": "course", "category": "DATA"})

    for idx, inventory in enumerate(cursor):
        pprint("{} - {}".format(idx, inventory), indent=4, compact=True)


def graph_content():

    G = nx.DiGraph()

    db = __get_db()
    cursor = db.inventory.find({"type": "course", "category": "data"})
    for doc_idx, document_dct in enumerate(cursor):

        G.add_node(document_dct["identifier"] + "-" + document_dct["label"])

        dependency_lst = document_dct.get("dependency_min_lst")
        # print(doc_idx, dependency_lst)
        if dependency_lst:

            for dependency_dct in dependency_lst:

                G.add_edges_from(
                    [
                        (
                            dependency_dct["identifier"]
                            + "-"
                            + dependency_dct["label"],
                            document_dct["identifier"] + "-" + document_dct["label"],
                        )
                    ]
                )

    # val_map = {'A': 1.0,
    #         'D': 0.5714285714285714,
    #         'H': 0.0}

    # values = [val_map.get(node, 0.25) for node in G.nodes()]

    # # Specify the edges you want here
    # red_edges = [('A', 'C'), ('E', 'C')]
    # edge_colours = ['black' if not edge in red_edges else 'red'
    #                 for edge in G.edges()]
    # black_edges = [edge for edge in G.edges() if edge not in red_edges]

    # # Need to create a layout when doing
    # # separate calls to draw nodes and edges
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
    #                     node_color = values, node_size = 500)
    # nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    # nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)

    options = {
        "node_color": "blue",
        "node_size": 100,
        "width": 3,
        "arrowstyle": "-|>",
        "arrowsize": 12,
    }

    # pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos=pos, arrows=True, **options)
    # nx.draw_circular(G, arrows=True, **options)
    # nx.draw_spectral(G, arrows=True, **options)

    pos = nx.nx_pydot.graphviz_layout(G)
    nx.draw_networkx(G, pos)

    plt.savefig("networkx_graph.png")

    # # pygraphviz
    # A = nx.nx_agraph.to_agraph(G)
    # A.layout()
    # A.draw('networkx_graph.png')

    # pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    # A = nx.nx_agraph.to_agraph(G)
    # nx.nx_agraph.write_dot(G, BASE_DIR)

    # # pydot
    # A = nx.nx_pydot.to_pydot(G)
    # nx.drawing.nx_pydot.write_dot(G, 'networkx_graph.png')
    # gv.render('dot', 'png', 'networkx_graph.png')

    plt.show()


def minimize_dependency():

    db = __get_db()
    cursor = db.inventory.find({"type": "course"})
    for doc_idx, document_dct in enumerate(cursor):

        dependency_lst = []
        if document_dct.get("dependency_lst"):
            dependency_lst = document_dct["dependency_lst"]
        dependency_min_lst = list(dependency_lst)
        logger.debug(
            "Root content: {}-{}".format(
                document_dct["identifier"], document_dct["label"]
            )
        )

        for dependency_idx, dependency_id_dct in enumerate(dependency_lst):

            child_dct = db.inventory.find(
                {"identifier": dependency_id_dct["identifier"]}
            )[0]
            __minimize_dependency(db, child_dct, dependency_min_lst)

        # Init. minimized dependency list
        update_res = db.inventory.update_one(
            {"identifier": document_dct["identifier"]},
            {
                "$set": {"dependency_min_lst": dependency_min_lst},
                "$currentDate": {"lastModified": True},
            },
        )
        logger.debug(
            "Update Minimized Dependency from {} to {}: {}, {}, {}, {}, {}".format(
                # content_idx,
                # content_dct["identifier"],
                # title,
                dependency_lst,
                dependency_min_lst,
                update_res.acknowledged,
                update_res.matched_count,
                update_res.modified_count,
                update_res.raw_result,
                update_res.upserted_id,
            )
        )


def __minimize_dependency(db, content_dct, root_dependency_min_lst):

    # Update. minimized dependency list
    n_dependency_min = len(root_dependency_min_lst)
    dependency_min_idx = 0
    logger.debug("Root dependency: {}".format(root_dependency_min_lst))
    logger.debug(
        "Current content: {}-{}".format(content_dct["identifier"], content_dct["label"])
    )

    dependency_lst = []
    if content_dct.get("dependency_lst"):
        dependency_lst = content_dct["dependency_lst"]

    while n_dependency_min > 1 and dependency_min_idx < n_dependency_min:

        # For each dependency child
        for dependency_idx, dependency_id_dct in enumerate(dependency_lst):

            # if a child is in minimized dependency list > remove child from list
            if dependency_id_dct in root_dependency_min_lst:
                root_dependency_min_lst.remove(dependency_id_dct)
                logger.debug("Remove : {}".format(dependency_id_dct))

            # Minimize with child
            child_dct = db.inventory.find(
                {"identifier": dependency_id_dct["identifier"]}
            )[0]
            __minimize_dependency(db, child_dct, root_dependency_min_lst)

        dependency_min_idx += 1
        n_dependency_min = len(root_dependency_min_lst)


def check_dependency_sanity():

    db = __get_db()
    cursor = db.inventory.find({"type": "course"})
    for doc_idx, document_dct in enumerate(cursor):

        __check_dependency(document_dct, [])


def __check_dependency(parent_dct, parent_id_lst):

    parent_id = parent_dct["identifier"]
    logger.debug("Parent ID: {}".format(parent_id))

    parent_id_lst.append((parent_id, parent_dct["label"]))

    parent_dependency_lst = parent_dct.get("dependency_lst")
    dependency_s = " > ".join(
        [
            "{}-{}-{}".format(content_idx, content_id_tup[0], content_id_tup[1])
            for content_idx, content_id_tup in enumerate(parent_id_lst)
        ]
    )
    logger.debug("Dependency: {}".format(dependency_s))

    if parent_dependency_lst:

        for idx, dependency_dct in enumerate(parent_dependency_lst):

            root_id = parent_id_lst[0][0]
            cur_id = dependency_dct["identifier"]
            logger.debug("Current ID: {}".format(cur_id))

            if cur_id == root_id:

                logger.warning("Loop: {}".format(dependency_s))

            else:
                db = __get_db()
                cursor = db.inventory.find({"identifier": cur_id})
                document_dct = cursor[0]

                __check_dependency(document_dct, parent_id_lst)
                pass

    else:
        logger.debug("No dependency")

    parent_id_lst.pop()


def __get_db():

    client = db_client.Connect.get_connection(
        zenvar.DB_HOST,
        zenvar.DB_PORT,
        zenvar.DB_AUTH_SOURCE,
        zenvar.DB_USR,
        zenvar.DB_PWD,
        zenvar.DB_NAME,
    )

    return client.test


if __name__ == "__main__":

    ocr_obj = OpenClassrooms()
    ocr_obj.get_posts(page_start_idx=4, n_page_max=0)

    # # =============================

    # # text_box = driver.find_element(by=By.NAME, value="my-text")
    # # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    # # text_box.send_keys("Selenium")
    # # submit_button.click()

    # # value = message.text

    # # answer = ""

    # # while answer != "q":
    # #     show_menu()
    # #     answer = input("Select an operation or type Q to quit:\n")
    # #     answer = answer.lower()
    # #     execute_operation(answer)
