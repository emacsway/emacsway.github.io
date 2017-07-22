import sqlparse
from storm.expr import (
    Add, Alias, build_tables, Column, COLUMN, Comparable, Count, EXPR, has_tables, In, LeftJoin,
    NamedFunc, Select, SQL, SQLRaw, Sum, Table as TableOrig, TABLE, Undef
)
from storm.databases.mysql import compile as compile
from storm.variables import Variable

compile = compile.create_child()


@compile.when(int, long)
def compile_int(compile, expr, state):
    return str(expr)


@compile.when(Variable)
def compile_variable(compile, variable, state):
    value = variable.get(to_db=True)
    if isinstance(value, (int, long)):
        return str(value)
    state.parameters.append(variable)
    return "?"


@compile.when(Select)
def compile_select(compile, select, state):
    tokens = ["SELECT "]
    state.push("auto_tables", [])
    state.push("context", COLUMN)
    if select.distinct:
        tokens.append("DISTINCT ")
        if isinstance(select.distinct, (tuple, list)):
            tokens.append(
                "ON (%s) " % compile(select.distinct, state, raw=True))
    tokens.append(compile(select.columns, state))
    tables_pos = len(tokens)
    parameters_pos = len(state.parameters)
    state.context = EXPR
    if select.where is not Undef:
        tokens.append(" WHERE ")
        tokens.append(compile(select.where, state, raw=True))
    if select.group_by is not Undef:
        tokens.append(" GROUP BY ")
        tokens.append(compile(select.group_by, state, raw=True))
    if select.having is not Undef:
        tokens.append(" HAVING ")
        tokens.append(compile(select.having, state, raw=True))
    if select.order_by is not Undef:
        tokens.append(" ORDER BY ")
        tokens.append(compile(select.order_by, state, raw=True))
    if select.limit is not Undef:  # patched
        tokens.append(" LIMIT ")
        tokens.append(compile(select.limit, state, raw=True))
    if select.offset is not Undef:  # patched
        tokens.append(" OFFSET ")
        tokens.append(compile(select.offset, state, raw=True))
    if has_tables(state, select):
        state.context = TABLE
        state.push("parameters", [])
        tokens.insert(tables_pos, " FROM ")
        tokens.insert(tables_pos+1, build_tables(compile, select.tables,
                                                 select.default_tables, state))
        parameters = state.parameters
        state.pop()
        state.parameters[parameters_pos:parameters_pos] = parameters
    state.pop()
    state.pop()
    return "".join(tokens)

S = SQL


def as_(self, name=Undef):
    return Alias(self, name)

Comparable.as_ = as_


class If(NamedFunc):
    __slots__ = ()
    name = "IF"


class Space(object):

    def __init__(self, factory):
        self._factory = factory

    def __getattr__(self, name):
        return self._factory(name)

C = Space(Column)


class Param(SQL):

    __slots__ = ()

    def __init__(self, expr):
        expr = '%({})s'.format(expr)
        SQL.__init__(self, expr)


P = Space(Param)


class Table(TableOrig):

    __slots__ = ()

    def __getattr__(cls, name):
        return Column(name, cls)

    def as_(cls, name=Undef):
        return TableAlias(cls, name)


T = Space(Table)


class TableAlias(Alias):

    def __getattr__(cls, name):
        return Column(name, cls)

# ============================================
# Ok,preparations is done, now let build query
# ============================================


class EventMapper(object):

    _compile = compile

    class BaseQuery(object):

        def __init__(self):
            meta_ta = T.stats_posts_meta.as_('i')
            self.event_where = []
            self.event_having = Add()
            self.event_query = self._create_event_query(self.event_where, self.event_having)
            self.info_query = self._create_info_query(TableAlias(self.event_query, 'e'), meta_ta)
            self.final_query = self._create_final_query(TableAlias(self.info_query, 'e'))

        def _create_event_query(self, where, having):
            event_ta = Table('entity_events_daily').as_('e')
            return Select(
                columns=[
                    Alias(None, 'TIMESTAMP'),
                    Alias(None, 'user_id'),
                    event_ta.entity_id.as_('entity_id'),
                ],
                tables=event_ta,
                where=(
                    (event_ta.site_id == P.site_id) &
                    (event_ta.category_id == P.category_id) &
                    (event_ta.timestamp >= P.min_timestamp) &
                    (event_ta.timestamp < P.max_timestamp) &
                    In(event_ta.event_id, where)
                ),
                group_by=[event_ta.entity_id],
                having=(
                    (C.created_entity_count >= P.min_entity_creation_count) &
                    (having > 0)
                )
            )

        def _create_info_query(self, event_query_ta, meta_ta):
            return Select(
                columns=[
                    Alias(None, 'entity_id'),
                    Alias(None, 'TIMESTAMP'),
                    Count().as_('active_entity_count'),
                    meta_ta.owner_id.as_('owner_id'),
                ],
                tables=LeftJoin(
                    event_query_ta,
                    meta_ta,
                    on=(meta_ta.entity_id == event_query_ta.entity_id)),
                group_by=[meta_ta.owner_id]
            )

        def _create_final_query(self, info_ta):
            return Select(
                columns=[SQLRaw('*')],
                tables=info_ta,
                offset=P.offset,
                limit=P.limit
            )

        def add_criteria(self, *names):
            for name in names:
                self.add_criterion(name)

        def add_criterion(self, name):
            count_name = "{}_count".format(name)
            self.event_query.columns.append(
                Sum(If(C.event_id.is_in(Param(name)), C.event_count, 0)).as_(count_name),
            )
            self.event_where.append(Param(name))
            self.event_having.exprs += (Column(count_name),)
            self.info_query.columns.append(
                Sum(Column(count_name)).as_(count_name)
            )

        def get(self):
            return self.final_query

    def find_by_criteria(self, **criteria):
        query = self.BaseQuery()
        query.add_criteria(*criteria.keys())
        return self._execute(query, criteria.values())

    def _execute(self, query, params=()):
        print sqlparse.format(self._compile(query.get()), reindent=True, keyword_case='upper')


event_mapper = EventMapper()
object_list = event_mapper.find_by_criteria(
    comments=1,
    internal_shares=2,
    external_shares=3,
    internal_likes=4,
    external_likes=5,
    entity_creations=6,
    views=7,
    clicks=8
)
