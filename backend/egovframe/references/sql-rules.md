# SQL Writing Rules

eGovFrame SQL writing rules (SQL 작성 규칙), from `egovframe-runtime/persistence-layer/sql-rule.md`. Rule numbers below are the guide's own numbers: "SQL rule N" for the rule summary table and "performance principle N" for 성능을 고려한 SQL 작성 원칙.

## Scope

- The guide states its purpose as unifying SQL style to improve readability. It is a writing standard, not a legal or inspection requirement. A project SQL standard, if one exists, takes precedence.
- The rules assume Oracle: the FAQ covers only `ORA-` errors, and terms such as "Precompiler", "Static Embedded SQL" and "센터컷" come from Oracle-centred standards. Some rules cannot be applied to other DBMSs.
- Performance principle 2 cites iBatis `<isNotEmpty>`. Apply it to MyBatis `<if test>` and other dynamic SQL tags as well.

## Detect the DBMS first

| Evidence | Where to look |
|----------|---------------|
| JDBC URL prefix: `jdbc:oracle:`, `jdbc:tibero:`, `jdbc:postgresql:`, `jdbc:mysql:`, `jdbc:mariadb:`, `jdbc:Altibase:` | `globals.properties`, `application.yml`/`.properties`, `context-datasource.xml` |
| `Globals.DbType` (e.g. `mysql`, `oracle`, `postgres`) | `globals.properties` in projects based on the common components |
| JDBC driver dependency | `pom.xml`, `build.gradle` |

Then apply the groups in this order:

| Group | Applies to | Report as |
|-------|------------|-----------|
| A. Common rules | Every DBMS | Violation (`R`) |
| B. Oracle-family rules | Oracle and Tibero only (Tibero compatibility is unverified: confirm with the project) | Violation (`R`) on Oracle family; not applicable elsewhere |
| C. Translated rules | Every DBMS, using the equivalent function | Violation (`R`) for the principle |
| D. Policy rules | Every DBMS | Item to confirm with the project (`G`), never a violation |

## A. Common rules

| Ref | Rule | Check |
|-----|------|-------|
| SQL rule 1 | Lines should be 80 columns or less and must not exceed 120 | Find lines longer than 120 characters in the SQL body |
| SQL rule 2 | Write SQL keywords in uppercase | Find lowercase `select`, `from`, `where` and so on |
| SQL rule 3 | Indent with spaces, never tabs | Search mapper XML for tab characters inside SQL |
| SQL rule 4, performance principle 6 | List only the columns the application uses; `SELECT *` is not allowed | Search for `SELECT *` and `A.*` |
| SQL rule 5 | Break lines at keywords, tables and columns | One column per line in SELECT, INSERT and UPDATE lists |
| SQL rule 6 | One space after a comma | Find `,X` with no space |
| SQL rule 7 | No space right after an opening parenthesis | Find `( X` |
| SQL rule 8 | Comments use `/* */`; `--` is not used | Search for `--` inside SQL |
| SQL rule 10, performance principle 10 | Every comparison value in WHERE is a bind variable; literal SQL is prohibited. In MyBatis use `#{}`; `${}` builds literal SQL and is also an SQL injection risk | Search for `${` and for quoted literals in WHERE |
| SQL rule 12, performance principle 3 | Inline views at most 3 levels deep (2 recommended) | Count nested `FROM (SELECT` levels |
| SQL rule 13 | Do not compare hard-coded data values in `DECODE` or `CASE WHEN` | Find `CASE WHEN X = '01'` style comparisons against literal codes |
| Layout examples | Leading commas; one column per line; table aliases `A`, `B`, `C` in FROM order; `AS` before every column alias; scalar subquery results always aliased | Review SELECT layout against these items |
| Layout examples | Right-align `SELECT`, `FROM`, `WHERE`, `AND` on the "T" of SELECT; INSERT clauses on the "T" of INSERT; UPDATE and DELETE clauses on the final "E" | Check keyword alignment |
| Layout examples | In WHERE, write join conditions before filter conditions | Check condition order |
| DELETE example | Never omit the WHERE clause of a DELETE | Find `DELETE FROM` without `WHERE` |
| Performance principle 5 | Do not transform columns in SELECT or WHERE without need (prevents index use) | Find functions applied to indexed columns in WHERE |
| Performance principle 9 | Use indexes to minimise sort operations when fetching maximum rows or sorted data | Review `ORDER BY` + `ROWNUM`/`LIMIT` queries |
| Performance principle 11 | Filter in WHERE rather than HAVING | Find HAVING conditions that do not use aggregates |
| Performance principle 13 | Minimise OR | Review long OR chains |
| Performance principle 14 | Use `UNION ALL` when the rows have no uniqueness constraint; do not use `UNION` | Search for `UNION` not followed by `ALL` |
| Performance principle 15 | Do not call INSERT, UPDATE or DELETE repeatedly in an application loop; process a collection at once | Find Mapper/DAO write calls inside `for`/`while` loops in Java |
| Performance principle 16 | At most 4 tables in FROM (3 join conditions) | Count tables per FROM clause |

## B. Oracle-family rules

| Ref | Rule | Why it is Oracle-only |
|-----|------|-----------------------|
| SQL rule 11 | ANSI SQL-92 join syntax (`JOIN ... ON`) is not used, except `FULL OUTER JOIN` when the business requires it | The rule assumes Oracle's `(+)` outer join. PostgreSQL and MySQL have no `(+)`, so outer joins there require ANSI syntax and this rule cannot be followed |
| SQL rule 9 | Hints use `/*+ */` only (never `--+`), and only `INDEX` and `INDEX_DESC`; any other hint needs agreement with the tuning owner | PostgreSQL has no built-in hints; MySQL uses the same comment syntax with different hint names |
| FAQ | Handling of `ORA-01555`, `ORA-01003`, `ORA-00600`, `ORA-00060` | Oracle error codes |

On a non-Oracle DBMS, state that SQL rules 9 and 11 do not apply instead of reporting them.

## C. Translated rules

| Ref | Rule | Application on other DBMSs |
|-----|------|----------------------------|
| Performance principle 7 | Use `CASE WHEN` rather than `DECODE` for multiple comparisons | `DECODE` is Oracle-specific; elsewhere `CASE` is the only option, so the rule is satisfied automatically |
| Performance principle 8 | Do not overuse `NVL` | Apply the same limit to `COALESCE`, `IFNULL`, `ISNULL` |
| SQL rule 14, performance principle 12 | Use static embedded SQL; `MERGE INTO` is allowed; `WITH` is allowed only in batch, never online | Keep the `WITH` restriction everywhere, but note that the stated reason (temporary tables) describes Oracle. `MERGE INTO` does not exist in MySQL |

## D. Policy rules

These rules state a limit without a technical reason or depend on screen type. Report them as items for the project to confirm.

| Ref | Rule |
|-----|------|
| Performance principle 1 | Do not access data through views for queries or changes |
| Performance principle 2 | Keep WHERE conditions static; do not abuse dynamic tags such as `<isNotEmpty>` (MyBatis `<if test>`) |
| Performance principle 4 | Do not transform data inside scalar subqueries; do not use scalar subqueries in batch programs |
| Performance principle 17 | Use analytic functions only on statistics screens |
| Performance principle 18 | Use scalar subqueries only on tables of 10,000 rows or fewer |

## Example

A SELECT written to the layout rules (Oracle family):

```sql
SELECT A.ID          AS ID        /* ID */
     , A.NAME        AS NAME      /* Name */
     , B.DEPT_NAME   AS DEPT_NAME /* Department name */
  FROM SAMPLE A                   /* Sample */
     , DEPT B                     /* Department */
 WHERE A.DEPT_ID = B.DEPT_ID
   AND A.USE_YN = #{useYn}
 ORDER BY A.ID
```

On PostgreSQL or MySQL, write the same query with `JOIN ... ON` when an outer join is needed, and keep every other rule.
