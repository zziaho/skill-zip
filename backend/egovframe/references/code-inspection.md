# Code Inspection (PMD)

The eGovFrame standard inspection ruleset, from `egovframe-development/implementation-tool/code-inspection.md` and `code-inspection-tool.md`. The guide states that code written when applying eGovFrame can be checked with this ruleset.

## Facts

- Tool: PMD. The ruleset file distributed with the guide is `EgovInspectionRules_kor-4.3.xml` (Korean messages).
- The ruleset has 44 rules selected from PMD. All are `R` in this skill because they form the official standard ruleset.
- The guide gives **no severity per rule and no pass/fail threshold**. Order findings by the security column first, then by impact.
- PMD in this ruleset does not detect SQL injection or XSS. The guide points to SpotBugs with FindSecurityBugs for those. Check `${}` in mapper XML separately (`sql-rules.md`, SQL rule 10).
- The rule names are standard PMD rule names. Configure them by these names in any PMD setup.

## Rules mapped to software security weaknesses

The guide maps these 10 rules to SW security weaknesses (SW 보안 약점). Review them first.

| No. | PMD rule | Detects | Security weakness (as listed in the guide) |
|-----|----------|---------|---------------------------------------------|
| 2 | ArrayIsStoredDirectly | A method stores an array argument directly in a private field | Private array returned from a public method |
| 6 | AvoidCatchingGenericException | Catching `Exception`, `RuntimeException` or `NullPointerException` | Improper exception handling |
| 7 | AvoidPrintStackTrace | `printStackTrace()` calls | Information exposure through error messages |
| 12 | AvoidUsingHardCodedIP | Hard-coded IP addresses | Hard-coded sensitive information |
| 13 | BrokenNullCheck | Null checks that still dereference null | Null pointer dereference |
| 14 | CloseResource | Connections, statements, streams not closed | Improper resource release |
| 16 | EmptyCatchBlock | Empty catch blocks | Empty catch block, no error handling |
| 22 | HardCodedCryptoKey | Hard-coded cryptographic keys | Hard-coded sensitive information |
| 27 | MethodReturnsInternalArray | A method returns an internal array directly | Public data assigned to a private array |
| 28 | MisplacedNullCheck | Null checks placed after the dereference | Null pointer dereference |

The guide's mapping for rules 2 and 27 looks swapped relative to the rule names; report the weakness that matches the actual code.

## Other rules

| No. | PMD rule | Detects |
|-----|----------|---------|
| 1 | AbstractClassWithoutAbstractMethod | Abstract class with no abstract method |
| 3 | AssignmentInOperand | Assignment inside an operand |
| 4 | AssignmentToNonFinalStatic | Unsafe assignment to a non-final static field |
| 5 | AvoidArrayLoops | Array copy by loop instead of `System.arraycopy()` |
| 8 | AvoidReassigningParameters | Reassigning method parameters |
| 9 | AvoidSynchronizedAtMethodLevel | Method-level `synchronized` instead of a block |
| 10 | AvoidThrowingNullPointerException | Throwing `NullPointerException` |
| 11 | AvoidThrowingRawExceptionTypes | Throwing raw `Exception`, `RuntimeException`, `Throwable`, `Error` |
| 15 | ConstantsInterface | Interface used only to hold constants |
| 17 | EmptyControlStatement | Empty `finally`, `if`, `try`, `while` blocks |
| 18 | EqualsNull | `equals(null)` comparisons |
| 19 | FieldNamingConventions | Field names with underscores (non-constant fields) |
| 20 | FinalFieldCouldBeStatic | `final` fields with constant values that could be `static` |
| 21 | FormalParameterNamingConventions | Parameter names with underscores |
| 23 | ImmutableField | Private fields assigned only in the constructor but not `final` |
| 24 | InefficientEmptyStringCheck | `String.trim().length()` for emptiness checks |
| 25 | InefficientStringBuffering | Non-literal concatenation inside `StringBuffer`/`StringBuilder` calls |
| 26 | LocalVariableNamingConventions | Non-final local variables with underscores |
| 29 | SimpleDateFormatNeedsLocale | `SimpleDateFormat` created without a `Locale` |
| 30 | SimplifyBooleanExpressions | Needless comparisons with boolean literals |
| 31 | StringInstantiation | `new String(...)` without need |
| 32 | StringToString | `toString()` on a `String` |
| 33 | SwitchStmtsShouldHaveDefault | `switch` without `default` |
| 34 | SystemPrintln | `System.out`/`System.err` printing instead of a logger |
| 35 | UncommentedEmptyMethodBody | Empty method body without a comment |
| 36 | UnnecessaryBoxing | Needless wrapper object creation |
| 37 | UnnecessaryConversionTemporary | Temporary objects when converting primitives to `String` |
| 38 | UnnecessaryImport | Unused or duplicate imports |
| 39 | UnnecessarySemicolon | Stray semicolons |
| 40 | UnusedFormalParameter | Unused method parameters |
| 41 | UnusedPrivateField | Unused private fields |
| 42 | UnusedPrivateMethod | Unused private methods |
| 43 | UselessParentheses | Needless parentheses |
| 44 | UselessStringValueOf | `String.valueOf` when appending to a `String` |

## Interaction with eGovFrame code

| Situation | Guidance |
|-----------|----------|
| ServiceImpl methods declared `throws Exception` (as in the official samples) | Allowed. Rule 11 concerns *throwing* raw types; use `throw processException("key")` instead of `throw new Exception(...)` |
| Catching `Exception` to wrap it | Rule 6 applies. Catch the specific exception, or pass the cause to `processException("key", e)` |
| Debug output | Rule 34 applies. Use SLF4J (`foundation.md`) |
| Keys, passwords, IPs in code or `globals.properties` | Rules 12 and 22 apply to code. For properties files, use the crypto service of the version file and keep secrets out of the repository |

## Running PMD

- In eGovFrame IDE (Eclipse based): install the PMD plugin and import the ruleset XML through Preferences, as the guide describes.
- In a build, the `maven-pmd-plugin` can reference the same ruleset file. The guide does not prescribe a build setup.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-pmd-plugin</artifactId>
    <configuration>
        <rulesets>
            <ruleset>${project.basedir}/config/pmd/EgovInspectionRules_kor-4.3.xml</ruleset>
        </rulesets>
    </configuration>
</plugin>
```

The ruleset path above is an example location; place the file where the project keeps build configuration.
