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
hash: "sha256:<hash of the body below the front-matter>"
---

# Target Screens

> Executable specification for each *screen* of the new system, derived from the legacy according to the mode approved in `screen_modernization_decision.md`. Textual content is preserved literally, unless explicit approval is given for linguistic review.
> Primary reading material for the coder. Each section is a contract.

## Summary

- **Mode applied**: <literal | modernized | hybrid>
- **Screens generated**: <N>
- **Adapter**: <slug>
- **Tokens consumed**: see `_reversa_sdd/design-system/tokens.md` and `tokens-derived.md` when applicable
- **Golden files**: <N> in `_reversa_sdd/screens/golden/` (manifest in `golden/manifest.yaml`)
- **Registered deviations**: <N> in `screen_deviation_log.md`

> If the legacy does not have a UI (batch system / API / daemon), replace this section with:
> "No screens detected. Agent skipped in `skipped` mode. Next agent: Inspector."

---

## Screen: <canonical-name>

**Origin**: `<legacy-file>:<line-or-paragraph>`
**Mode applied**: literal | modernized
**Design-system components**: [<token1>, <token2>, ...]
**Interpolation points**: `{{var1}}`, `{{var2}}`
**Output transitions**: [<next screen or event>]
**Critical screen?**: yes | no (consult `reversa-detective` when available)

### Specification

> The block below varies depending on the source→target pair and the mode. See `references/adapter-pairs.md` for the canonical format of each pair. Examples below.

#### Example: COBOL TUI → Go CLI/TUI (literal)

```yaml
spec.kind: ansi-byte-stream
spec.normalize:
  - trim_trailing_spaces: false
  - line_endings: "\n"
spec.lines:
  - bytes: "\x1b[96m╔══════════════════════════════════════════════════╗\x1b[0m\n"
  - bytes: "\x1b[96m║                \x1b[93m▓▓▓ BANK ATM ▓▓▓\x1b[96m               ║\x1b[0m\n"
  - bytes: "\x1b[96m║                  \x1b[97m{{header_subtitle}}\x1b[96m                ║\x1b[0m\n"
    interpolations:
      header_subtitle:
        type: string
        max_width: 16
        source: literal "Caixa Eletronico" | literal "Acesso ao Sistema"
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
      submit_event: cliente.create
      children:
        - component: FormField
          name: nome
          label: "Full name"
          legacy_origin: "TForm1.edtNome"
          validation:
            required: true
            max_length: 80
        - component: FormField
          name: cpf
          label: "CPN"
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
          legacy_origin: "TForm1.btnSalvar"
          action: form.submit
        - component: Button
          variant: ghost
          label: "Cancel"
          legacy_origin: "TForm1.btnCancelar"
          action: navigate.back
spec.state_messages:
  loading: "Saving..."
  error: "{{error_message}}"
  success: "Customer successfully registered."
```

#### Example: Legacy server-rendered HTML → Componentized SPA (modernized)

```yaml
spec.kind: route-component
spec.route: /clientes/novo
spec.layout: AppLayout
spec.states: [idle, loading, error, success]
spec.component:
  component: ClientesNovoPage
  legacy_origin: "/admin/cliente_novo.asp"
  state:
    cliente:
      type: Cliente
      initial: empty
  children:
    - component: PageTitle
      content: "New Customer"
    - component: ClienteForm
      props:
        onSubmit: clienteService.create
        initial: $state.cliente
spec.api_changes:
  - legacy: POST /admin/cliente_novo.asp (form-urlencoded)
    target: POST /api/clientes (application/json)
    deviation: DEV-014
```

#### Example: Android XML → Flutter (modernized)

```yaml
spec.kind: composable
spec.name: ClienteListScreen
spec.legacy_origin: "app/src/main/res/layout/activity_cliente_list.xml + ClienteListActivity.java"
spec.states: [idle, loading, error, success]
spec.composable: |
  Scaffold(
    appBar: AppBar(title: Text("Customers")),
    body: Consumer<ClienteListVM>(
      builder: (ctx, vm, _) => vm.loading
        ? CircularProgressIndicator()
        : ListView.builder(
            itemCount: vm.clientes.length,
            itemBuilder: (_, i) => ClienteListTile(cliente: vm.clientes[i]),
          ),
    ),
    floatingActionButton: FloatingActionButton(
      onPressed: () => Navigator.pushNamed(ctx, '/clientes/novo'),
      child: Icon(Icons.add),
    ),
  )
spec.viewmodel:
  name: ClienteListVM
  legacy_origin: "ClienteListActivity.onResume"
  methods:
    - load(): calls clienteService.listar
```

### Accepted Divergence Points

- DEV-XXX: <short description> (see `screen_deviation_log.md#DEV-XXX`)

### States (modernized mode only)

| State | Description | Content / Message |
|---|---|---|
| Idle | Default state before any action | <content> |
| Loading | Asynchronous operation in progress | <spinner / skeleton> |
| Error | Failure in the operation or invalid data | `{{error_message}}` |
| Success | Operation completed successfully | <confirmation message> |

> In literal mode, this section can be omitted or replaced with "preserves the states of the legacy" if the legacy does not have an explicit disposition of states.

---

## Screen: <second-screen>

(repeat the block above for each screen)

---

## Appendix: Traceability to inventory

| Screen from `target_screens.md` | Origin in `_reversa_sdd/ui/inventory.md` | Origin in `_reversa_sdd/screens/inventory.json` |
|---|---|---|
| <screen 1> | <line from the inventory> | <internal inventory id> |
| <screen 2> | <line from the inventory> | <internal inventory id> |
```