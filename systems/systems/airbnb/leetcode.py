"""Airbnb System Design."""
import sys
from hornet.digraph import Digraph, SubGraph, Cluster
from systems.nodes import (
    Kafka,
    Elasticsearch,
    Cassandra,
    Internet,
    NextJs,
    Redis,
    HAProxy,
    Spring,
    Python,
    PostgreSQL,
)


if __name__ == "__main__":
    """Draw an Airbnb system architecture."""
    with Digraph(
        sys.argv[1],
        {
            "dpi": "350",
            "splines": "true",
            "newrank": "true",
            "fontname": "Times New Roman",
        },
        cleanup=False,
    ):
        internet = Internet("Internet")
        with Cluster():
            with SubGraph({"rank": "same"}):
                frontend = NextJs("Frontend")
                api_gateway = Spring("API Gateway")
                frontend >> api_gateway

            load_balancer = HAProxy("Load Balancer")
            load_balancer >> frontend
            api_gateway >> Spring("User") >> PostgreSQL("DB")
            internet >> [load_balancer, api_gateway]
            hotel = Spring("Hotel")
            api_gateway >> hotel >> PostgreSQL("DB")
            booking = Spring("Booking")
            api_gateway >> booking
            (
                api_gateway
                >> Spring("Hotel")
                >> [
                    PostgreSQL("DB"),
                    Redis("Cache"),
                    Elasticsearch("Search"),
                ]
            )

            booking >> [PostgreSQL("DB")]

            messages = Kafka("User activities")
            analysis = Python("Analysis")

            (
                [hotel, booking]
                >> messages
                << analysis
                >> Cassandra("User activities")
            )
