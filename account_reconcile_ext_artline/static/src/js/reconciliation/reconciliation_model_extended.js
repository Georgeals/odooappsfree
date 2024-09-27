odoo.define('account_reconcile_ext_artline.ReconciliationModelExtended', function (require) {
"use strict";

var Reconciliation = require('account.ReconciliationModel');


Reconciliation.StatementModel.include({
    _formatLine: function (lines) {
        var self = this;
        var defs = [];

        // remove reconciliation_proposition if no linked partner to line
        for (let line of lines) {
            if (line.st_line.partner_id === false) {
                line.reconciliation_proposition = [];
            }
        };

        _.each(lines, function (data) {
            var line = _.find(self.lines, function (l) {
                return l.id === data.st_line.id;
            });
            line.visible = true;
            line.limitMoveLines = self.limitMoveLines;
            _.extend(line, data);
            self._formatLineProposition(line, line.reconciliation_proposition);
            if (!line.reconciliation_proposition.length) {
                delete line.reconciliation_proposition;
            }
            defs.push(self._computeLine(line));
        });
        return $.when.apply($, defs);
    },
});
});
