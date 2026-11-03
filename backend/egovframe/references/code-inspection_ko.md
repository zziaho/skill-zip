# 코드 점검 (PMD)

`egovframe-development/implementation-tool/code-inspection.md`와 `code-inspection-tool.md`에 실린 eGovFrame 표준 Inspection 룰셋을 다룹니다. 가이드는 eGovFrame을 적용할 때 이 룰셋으로 소스 코드를 검사할 수 있다고 설명합니다.

## 기본 사항

- 도구는 PMD입니다. 가이드와 함께 배포되는 룰셋 파일은 `EgovInspectionRules_kor-4.3.xml`(한국어 메시지판)입니다.
- 룰셋은 PMD 규칙 중에서 고른 44개 규칙으로 구성됩니다. 공식 표준 룰셋이므로 이 스킬에서는 모두 `R`로 취급합니다.
- 가이드에는 **규칙별 심각도와 통과 기준이 없습니다.** 보안 약점 열에 해당하는 규칙을 먼저 보고하고, 그다음에 영향이 큰 순서로 보고합니다.
- 이 룰셋의 PMD 규칙으로는 SQL 인젝션과 XSS를 찾을 수 없습니다. 가이드는 이런 취약점을 찾을 때 SpotBugs와 FindSecurityBugs를 사용하라고 안내합니다. 매퍼 XML의 `${}`는 따로 확인합니다(`sql-rules_ko.md`의 SQL 규칙 10).
- 규칙 이름은 PMD의 표준 규칙 이름입니다. 어떤 PMD 설정에서든 이 이름으로 규칙을 지정합니다.

## SW 보안 약점과 연결된 규칙

가이드는 다음 10개 규칙을 SW 보안 약점과 연결해 두었습니다. 이 규칙들을 먼저 검토합니다.

| 번호 | PMD 규칙 | 찾아내는 코드 | 보안 약점 (가이드 표기) |
|------|----------|---------------|--------------------------|
| 2 | ArrayIsStoredDirectly | 메서드가 인자로 받은 배열을 private 필드에 그대로 저장하는 코드 | Public 메소드부터 반환된 Private 배열 |
| 6 | AvoidCatchingGenericException | `Exception`, `RuntimeException`, `NullPointerException`을 catch하는 코드 | 부적절한 예외처리 |
| 7 | AvoidPrintStackTrace | `printStackTrace()` 호출 | 오류 메시지를 통한 정보 노출 |
| 12 | AvoidUsingHardCodedIP | 하드코딩된 IP 주소 | 하드코드된 중요정보 |
| 13 | BrokenNullCheck | null을 확인하고도 null을 역참조하는 코드 | 널(Null) 포인터 역참조 |
| 14 | CloseResource | 닫지 않은 커넥션, 스테이트먼트, 스트림 | 부적절한 자원 해제 |
| 16 | EmptyCatchBlock | 비어 있는 catch 블록 | 빈 Catch 문 사용, 오류 상황 대응 부재 |
| 22 | HardCodedCryptoKey | 하드코딩된 암호화 키 | 하드코드된 중요정보 |
| 27 | MethodReturnsInternalArray | 내부 배열을 그대로 반환하는 메서드 | Private 배열에 Public 데이터 할당 |
| 28 | MisplacedNullCheck | 역참조한 뒤에 null을 확인하는 코드 | 널(Null) 포인터 역참조 |

가이드에서 2번과 27번 규칙에 연결된 보안 약점은 규칙 이름과 비교하면 서로 바뀌어 있는 것으로 보입니다. 보고할 때는 실제 코드에 해당하는 보안 약점을 적습니다.

## 그 밖의 규칙

| 번호 | PMD 규칙 | 찾아내는 코드 |
|------|----------|---------------|
| 1 | AbstractClassWithoutAbstractMethod | 추상 메서드가 없는 추상 클래스 |
| 3 | AssignmentInOperand | 피연산자 안에서 값을 할당하는 코드 |
| 4 | AssignmentToNonFinalStatic | final이 아닌 static 필드에 안전하지 않게 값을 할당하는 코드 |
| 5 | AvoidArrayLoops | `System.arraycopy()` 대신 반복문으로 배열을 복사하는 코드 |
| 8 | AvoidReassigningParameters | 메서드 파라미터에 값을 다시 할당하는 코드 |
| 9 | AvoidSynchronizedAtMethodLevel | 블록 대신 메서드 단위로 선언한 `synchronized` |
| 10 | AvoidThrowingNullPointerException | `NullPointerException`을 직접 throw하는 코드 |
| 11 | AvoidThrowingRawExceptionTypes | 가공하지 않은 `Exception`, `RuntimeException`, `Throwable`, `Error`를 throw하는 코드 |
| 15 | ConstantsInterface | 상수만 담는 인터페이스 |
| 17 | EmptyControlStatement | 비어 있는 `finally`, `if`, `try`, `while` 블록 |
| 18 | EqualsNull | `equals(null)` 비교 |
| 19 | FieldNamingConventions | 밑줄이 들어간 필드 이름(상수 제외) |
| 20 | FinalFieldCouldBeStatic | 상수 값을 가지므로 `static`으로 바꿀 수 있는 `final` 필드 |
| 21 | FormalParameterNamingConventions | 밑줄이 들어간 파라미터 이름 |
| 23 | ImmutableField | 생성자에서만 값을 할당하는데도 `final`로 선언하지 않은 private 필드 |
| 24 | InefficientEmptyStringCheck | 빈 문자열인지 확인하려고 `String.trim().length()`를 사용하는 코드 |
| 25 | InefficientStringBuffering | `StringBuffer`·`StringBuilder` 호출 안에서 리터럴이 아닌 값을 이어 붙이는 코드 |
| 26 | LocalVariableNamingConventions | 밑줄이 들어간 final이 아닌 지역 변수 |
| 29 | SimpleDateFormatNeedsLocale | `Locale` 없이 생성한 `SimpleDateFormat` |
| 30 | SimplifyBooleanExpressions | boolean 리터럴과 불필요하게 비교하는 코드 |
| 31 | StringInstantiation | 불필요한 `new String(...)` |
| 32 | StringToString | `String`에 `toString()`을 호출하는 코드 |
| 33 | SwitchStmtsShouldHaveDefault | `default`가 없는 `switch` |
| 34 | SystemPrintln | 로거 대신 `System.out`·`System.err`로 출력하는 코드 |
| 35 | UncommentedEmptyMethodBody | 주석 없이 비어 있는 메서드 본문 |
| 36 | UnnecessaryBoxing | 불필요한 래퍼 객체 생성 |
| 37 | UnnecessaryConversionTemporary | 기본형을 `String`으로 바꿀 때 만드는 불필요한 임시 객체 |
| 38 | UnnecessaryImport | 사용하지 않거나 중복된 import |
| 39 | UnnecessarySemicolon | 불필요한 세미콜론 |
| 40 | UnusedFormalParameter | 사용하지 않는 메서드 파라미터 |
| 41 | UnusedPrivateField | 사용하지 않는 private 필드 |
| 42 | UnusedPrivateMethod | 사용하지 않는 private 메서드 |
| 43 | UselessParentheses | 불필요한 괄호 |
| 44 | UselessStringValueOf | `String`에 이어 붙일 때 사용하는 불필요한 `String.valueOf` |

## eGovFrame 코드에 적용할 때

| 상황 | 안내 |
|------|------|
| ServiceImpl 메서드에 `throws Exception`을 선언한 경우(공식 샘플과 같은 방식) | 허용됩니다. 11번 규칙은 가공하지 않은 예외를 *throw하는 코드*를 대상으로 합니다. `throw new Exception(...)` 대신 `throw processException("key")`를 사용합니다 |
| 예외를 감싸려고 `Exception`을 catch하는 경우 | 6번 규칙에 해당합니다. 구체적인 예외를 catch하거나, 원인 예외를 `processException("key", e)`로 넘깁니다 |
| 디버그 출력 | 34번 규칙에 해당합니다. SLF4J를 사용합니다(`foundation_ko.md`) |
| 코드나 `globals.properties`에 들어 있는 키, 비밀번호, IP | 코드에는 12번과 22번 규칙이 적용됩니다. 프로퍼티 파일은 버전 파일에 있는 암호화 서비스를 사용하고, 비밀 정보는 저장소에 올리지 않습니다 |

## PMD 실행

- eGovFrame IDE(Eclipse 기반)에서는 가이드의 설명대로 PMD 플러그인을 설치하고, Preferences에서 룰셋 XML을 가져옵니다.
- 빌드에서는 `maven-pmd-plugin`이 같은 룰셋 파일을 참조할 수 있습니다. 빌드 설정 방식은 가이드에 정해져 있지 않습니다.

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

위의 룰셋 경로는 예시입니다. 프로젝트에서 빌드 설정을 보관하는 위치에 파일을 둡니다.
