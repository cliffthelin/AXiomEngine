### Platform Detection

Heuristics used by `reversa-screen-translator` to classify the origin platform of legacy code based on the content of `_reversa_sdd/inventory.md` and the source code. Use in conjunction with `references/adapter-pairs.md` to choose the adapter.

The confidence scale applied for classification:

- 🟢 **CONFIRMED**: At least one strong signature (header, namespace, unique marker) is present.
- 🟡 **INFERRED**: Extension and general pattern match, but no unique signature.
- 🔴 **GAP**: Missing source code artifact; classifies only based on `inventory.md`.
- ⚠️ **AMBIGUOUS**: Two plausible platforms are tied (e.g., classic ASP vs ASP.NET WebForms in older projects).

## Signature Table

| Origin Slug | Typical Extension | Strong Signature | Weak Signature |
|---|---|---|---|
| `cobol-ansi-tui` | `.cob`, `.cbl`, `.cpy` | `PROCEDURE DIVISION.` + `DISPLAY`/`ACCEPT` + sequences `\x1B[`, box-drawing Unicode (`╔ ╗ ┌ ┐`) | `PROCEDURE DIVISION` only (without ANSI = batch COBOL) |
| `cobol-screen-section` | `.cob`, `.cbl` | `SCREEN SECTION` + attributes `LINE`, `COLUMN`, `FOREGROUND-COLOR` | `SCREEN SECTION` without details |
| `ncurses-c` | `.c`, `.h` | `#include <ncurses.h>` or `<curses.h>` + `WINDOW *`, `wprintw`, `mvwaddstr` | `printf` + `\033[` (handcrafted TUI) |
| `delphi-vcl` | `.pas`, `.dfm`, `.dpr` | `unit `, `interface`, `TForm`, `TPanel`, `TButton` in `.dfm` | Pure `.pas` without `.dfm` (likely CLI) |
| `delphi-firemonkey` | `.pas`, `.fmx` | `TForm` in `.fmx` file (FireMonkey) | `.pas` only |
| `vb6` | `.frm`, `.bas`, `.cls`, `.vbp` | `VERSION 5.00` in header, `Begin VB.Form`, `Begin VB.CommandButton` | Pure `.bas` (module without UI) |
| `vbnet-winforms` | `.vb` + `Designer.vb` | `Inherits System.Windows.Forms.Form` | `Module ... Sub Main` only (CLI) |
| `csharp-winforms` | `.cs`, `.designer.cs` | `using System.Windows.Forms;` + `partial class ... : Form` | `using System;` only |
| `csharp-wpf` | `.xaml`, `.cs` | `xmlns="http://schemas.microsoft.com/winfx/..."` + `<Window>`, `<Grid>` | `.cs` only without `.xaml` |
| `win32-mfc` | `.cpp`, `.h`, `.rc` | `BEGIN_MESSAGE_MAP`, `CDialog`, `WinMain`, `IDD_*` in `.rc` | `WinMain` alone |
| `win32-raw` | `.cpp`, `.h` | `WinMain` + `RegisterClass`, `CreateWindow`, `WM_*` messages | `WinMain` only |
| `asp-classic` | `.asp`, `.inc` | `<%@ Language=VBScript %>` or `<%@ Language=JScript %>` + `Response.Write` | `.asp` without `<%@` |
| `aspnet-webforms` | `.aspx`, `.aspx.cs`, `.aspx.vb` | `<%@ Page Language="C#"`, `runat="server"`, `<asp:` controls | Simple `.aspx` only |
| `jsp` | `.jsp`, `.jspf` | `<%@ page language="java" %>`, `<jsp:`, `<%! %>` | `.jsp` with only HTML |
| `php-server-rendered` | `.php` | `<?php ... ?>` + inline HTML + `mysql_*` or `mysqli_*` | `.php` only in `api/` folder (probably a REST API, not UI) |
| `html-legacy-jquery` | `.html`, `.htm`, `.js` | `jQuery`/`$.ajax` + form submits server-side, no SPA framework | Static HTML (no dynamic JS) |
| `android-xml-java` | `res/layout/*.xml`, `*.java` | `<LinearLayout>`/`<RelativeLayout>`/`<ConstraintLayout>` + `Activity extends`, `setContentView(R.layout...)` | Java only without `res/layout/` |
| `android-xml-kotlin` | `res/layout/*.xml`, `*.kt` | Same as above + `Activity()` Kotlin + `setContentView(R.layout...)` | Kotlin only without `res/layout/` |
| `android-compose` | `*.kt` | `@Composable`, `setContent { ... }` | without `setContent` |
| `ios-xib-objc` | `.xib`, `.m`, `.h`, `.storyboard` | `UIViewController` + `*.xib` or `*.storyboard` referenced | `*.m` only without XIB |
| `ios-xib-swift` | `.xib`, `.swift`, `.storyboard` | `UIViewController` Swift + XIB/Storyboard | `*.swift` only without XIB |
| `ios-swiftui` | `*.swift` | `View` + `var body: some View`, `App` lifecycle | without `var body` |
| `flutter` | `*.dart`, `pubspec.yaml` | `import 'package:flutter/material.dart'` + `StatelessWidget`/`StatefulWidget` | without `material.dart` |
| `react-class` | `*.jsx`, `*.tsx` | `class ... extends React.Component` + `render()` | `*.tsx` only (probably modern) |
| `react-hooks` | `*.jsx`, `*.tsx` | `function ... ({...}) { return <...>; }` + `useState`, `useEffect` | (not legacy, this is the target) |

## Additional Indicators

- **Directory structure**:
  - `forms/`, `Forms/` → Delphi, VB6, .NET WinForms.
  - `views/`, `templates/` → Server-side MVC (ASP, JSP, PHP).
  - `app/src/main/res/layout/` → Android.
  - `Storyboard.storyboard` or `*.xib` in the root → Legacy iOS.
  - `Pages/` in a Razor project → ASP.NET.
- **Build files**:
  - `*.dpr` (Delphi), `*.vbp` (VB6), `*.csproj` (.NET), `pom.xml`/`build.gradle` (Java/Android), `Podfile` (iOS), `pubspec.yaml` (Flutter).
- **Version strings in comments or headers**: VB6 marks `VERSION 5.00`; Delphi 7 marks `{$OBJECT}`; .NET with `<TargetFramework>net48</TargetFramework>` indicates legacy WinForms.

## When two platforms are tied

- **Classic ASP vs ASP.NET WebForms**: `.asp` files without `.aspx` → classic. `.aspx` + `.asp` in the same project → project migrating, mark ⚠️ AMBIGUOUS and ask.
- **VB6 vs VB.NET**: `.frm` + `.vbp` → VB6. `.vb` + `.designer.vb` + `.vbproj` → VB.NET WinForms.
- **Delphi VCL vs FireMonkey**: `.dfm` → VCL. `.fmx` → FireMonkey. Both in the project → mark ⚠️ AMBIGUOUS.
- **Android Java vs Kotlin**: `.java` + `.kt` in the same project → project in migration; classify by individual file.
- **iOS Storyboard vs XIB**: both supported; treat as a class (`ios-*`). The difference lies in the detail of capture.

## When nothing matches

Register `EC-01` (unknown origin platform) and offer the user a "raw" template where they describe the screen in structured prose, with required sections:

- Identity.
- Layout in ASCII art or screenshot.
- List of fields / components.
- Literal messages / labels.
- Events and transitions.
- Validations.

The agent then generates `target_screens.md` with `spec.kind: raw-prose` and marks in `screen_deviation_log.md` that the screen did not go through the adapter.