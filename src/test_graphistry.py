import pandas as pd
import neo4j # just for testing
from neo4j import GraphDatabase # for data loader
import graphistry
print('neo4j', neo4j.__version__)
print('graphistry', graphistry.__version__)


NEO4J = {
    'uri': host,
    'auth': (user, password)
}
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", personal_key_id="KN6Z3X4IYJ", personal_key_secret="Z2YN24MVKMS007HU")
graphistry.register(bolt=NEO4J)

# To specify Graphistry account & server, use:
# graphistry.register(api=3, username='...', password='...', protocol='https', server='hub.graphistry.com')
# For more options, see https://github.com/graphistry/pygraphistry#configure



g = graphistry.cypher("""
    MATCH (m)
    RETURN m LIMIT 200
    """)
g.plot()

