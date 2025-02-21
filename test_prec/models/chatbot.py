from odoo import models, fields, api

class ChatBot(models.AbstractModel):
    _name = 'chat.bot'
    _description = 'Chat Bot Model'

    def reply_from_bot(self, record, values, command=None):
        bot_id = self.env['ir.model.data']._xmlid_to_res_id("test_prec.bot_partner")
        if len(record) != 1 or values.get("author_id") == bot_id or values.get("message_type") != "comment" and not command:
            return
        if bot_id in values.get('partner_ids', []) or self._is_bot_in_private_channel(record):
            body = values.get("body", "").replace(u'\xa0', u' ').strip().lower().strip(".!")
            answer = self._get_answer(record, body, values, command)
            if answer:
                message_type = 'comment'
                subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')
                record.with_context(mail_create_nosubscribe=True).sudo().message_post(body=answer, author_id=bot_id, message_type=message_type, subtype_id=subtype_id)

    def _is_bot_in_private_channel(self, record):
        bot_id = self.env['ir.model.data']._xmlid_to_res_id("test_prec.bot_partner")
        if record._name == 'discuss.channel' and record.channel_type == 'chat':
            return bot_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False

    def _get_answer(self, record, body, values, command):
        return "you said: " + body + " and I am a bot"

