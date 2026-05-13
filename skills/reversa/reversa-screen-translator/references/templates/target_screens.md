```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_screens
producedBy: screen-translator
mode: literal | modernized | hybrid
sourcePlatform: <slug>
targetPlatform: <slug>
adapter: <adapters/origem__alvo>
screenCount: <int>
hash: "sha256:<hash do corpo abaixo do front-matter>"
---

# Target Screens

> Executable specification of each screen in the new system, derived from the legacy system according to the approved mode in `screen_modernization_decision.md`. Textual content preserved literally, unless explicit linguistic review approval is granted. A primary reference for the developer. Each section is a contract.

## Summary

-   **Mode applied**: <literal | modernized | hybrid>
-   **Screens generated**: <N>
-   **Adapter**: <slug>
-   **Tokens consumed**: see `_reversa_sdd/design-system/tokens.md` and `tokens-derived.md` when applicable
-   **Golden files**: <N> in `_reversa_sdd/screens/golden/` (manifest in `golden/manifest.yaml`)
-   **Registered deviations**: <N> in `screen_deviation_log.md`

> If the legacy system does not have a UI (batch system / API / daemon), replace this section with: "No screens detected. Agent skipped in `skipped` mode. Next agent: Inspector."

---

## Screen: <nome-canonical>

**Source**: `<arquivo-legado>:<linha-ou-paragrafo>`
**Mode applied**: literal | modernized
**Design-system components**: [<token1>, <token2>, ...]
**Interpolation points**: `{{var1}}`, `{{var2}}`
**Outgoing transitions**: [<next screen or event>]
**Critical screen?**: yes | no (check `reversa-detective` when available)

### Specification

> The block below varies according to the source→target pair and the mode. See `references/adapter-pairs.md` for the canonical format of each pair. Examples below.

#### Example: COBOL TUI → Go CLI/TUI (literal)

```yaml
spec.kind: ansi-byte-stream
spec.normalize:
  - trim_trailing_spaces: false
  - line_endings: "\n"
spec.lines:
  - bytes: "\x1b[96m╔══════════════════════════════════════════════════╗\x1b[0m\n"
  - bytes: "\x1b[96m║                \x1b[93m▓▓▓  BANK ATM  ▓▓▓\x1b[96m               ║\x1b[0m\n"
  - bytes: "\x1b[96m║                  \x1b[97m{{header_subtitle}}\x1b[96m                ║\x1b[0m\n"
    interpolations:
      header_subtitle:
        type: string
        max_width: 16
        source: literal "Cash Machine" | literal "System Access"
  - bytes: "\x1b[96m╚══════════════════════════════════════════════════╝\x1b[0m\n"
spec.input_prompts:
  - kind: accept-line
    prompt_bytes: "   \x1b[96m>>\x1b[97m Select an option: \x1b[0m"
    captures: opcao
    valid: ["0", "1", "2", "3", "4", "5"]
```

#### Example: Win32/Delphi VCL → Web SPA (modernized)

```yaml
spec.kind: component-tree
spec.states: [idle, loading, error, success]
spec.root:
  component: PageLayout
  variant: form
  children:
    - component: Header
      tokens: [color.brand-primary, typography.h1]
      content:
        text: "Register Customer"
    - component: Form
      submit_event: client.create
      children:
        - component: FormField
          name: name
          label: "Full name"
          legacy_origin: "TForm1.edtName"
          validation:
            required: true
            max_length: 80
        - component: FormField
          name: cpf
          label: "CPF"
          legacy_origin: "TForm1.mskCPF"
          mask: "999.999.999-99"
          validation:
            required: true
            cpf: true
    - component: ButtonRow
      children:
        - component: Button
          variant: primary
          label: "Save"
          legacy_origin: "TForm1.btnSave"
          action: form.submit
        - component: Button
          variant: ghost
          label: "Cancel"
          legacy_origin: "TForm1.btnCancel"
          action: navigate.back
spec.state_messages:
  loading: "Saving..."
  error: "{{error_message}}"
  success: "Customer registered successfully."
```

#### Example: Legacy server-rendered HTML → Componentized SPA (modernized)

```yaml
spec.kind: route-component
spec.route: /customers/new
spec.layout: AppLayout
spec.states: [idle, loading, error, success]
spec.component:
  component: CustomersNewPage
  legacy_origin: "/admin/client_new.asp"
  state:
    customer:
      type: Customer
      initial: empty
  children:
    - component: PageTitle
      content: "New Customer"
    - component: CustomerForm
      props:
        onSubmit: customerService.create
        initial: $state.customer
spec.api_changes:
  - legacy: POST /admin/client_new.asp (form-urlencoded)
    target: POST /api/customers (application/json)
    deviation: DEV-014
```

#### Example: Android XML → Flutter (modernized)

```yaml
spec.kind: composable
spec.name: CustomerListScreen
spec.legacy_origin: "app/src/main/res/layout/activity_customer_list.xml + CustomerListActivity.java"
spec.states: [idle, loading, error, success]
spec.composable: |
  Scaffold(
    appBar: AppBar(title: Text("Customers")),
    body: Consumer<CustomerListVM>(
      builder: (ctx, vm, _) => vm.loading
        ? CircularProgressIndicator()
        : ListView.builder(
            itemCount: vm.customers.length,
            itemBuilder: (_, i) => CustomerListTile(customer: vm.customers[i]),
          ),
    ),
    floatingActionButton: FloatingActionButton(
      onPressed: () => Navigator.pushNamed(ctx, '/customers/new'),
      child: Icon(Icons.add),
    ),
  )
spec.viewmodel:
  name: CustomerListVM
  legacy_origin: "CustomerListActivity.onResume"
  methods:
    - load(): calls customerService.list
```

### Accepted divergence points

-   DEV-XXX: <short description> (see `screen_deviation_log.md#DEV-XXX`)

### States (modernized mode only)

| State  | Description                       | Content / message |
| ------ | --------------------------------- | ----------------- |
| Idle   | Default state before any action   | <content>         |
| Loading | Asynchronous operation in progress | <spinner / skeleton> |
| Error  | Operation failure or invalid data  | `{{error_message}}` |
| Success | Operation completed successfully  | <confirmation message> |

> In literal mode, this section can be omitted or replaced with "preserves the legacy states" if the legacy system does not have an explicit definition of states.

---

## Screen: <segunda-tela>

(repeat the block above for each screen)

---

## Appendix: traceability to inventory

| Screen in `target_screens.md` | Source in `_reversa_sdd/ui/inventory.md` | Source in `_reversa_sdd/screens/inventory.json` |
| ----------------------------- | ---------------------------------------- | ----------------------------------------------- |
| <screen 1>                    | <line in the inventory>                | <internal inventory id>                        |
| <screen 2>                    | <line in the inventory>                | <internal inventory id>                        |
```