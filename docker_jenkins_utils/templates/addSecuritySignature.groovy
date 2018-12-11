import org.jenkinsci.plugins.scriptsecurity.scripts.*
signature = "{{ signature }}"
ScriptApproval.PendingSignature s = new ScriptApproval.PendingSignature(signature, false, ApprovalContext.create())

ScriptApproval sa = ScriptApproval.get();
sa.approveSignature(s.signature);