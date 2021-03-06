function() {

    var or3client = lib.or3client;

    var CONFERENCE = 'auai.org/UAI/2017';
    var COCHAIRS = 'auai.org/UAI/2017/Program_Co-Chairs';
    var SPC = 'auai.org/UAI/2017/Senior_Program_Committee';
    var PC = 'auai.org/UAI/2017/Program_Committee';

    var referenceInvite = {
      id: CONFERENCE + '/-/Paper' + note.number + '/Add/Revision',
      signatures: [CONFERENCE],
      writers: [CONFERENCE],
      invitees: note.content.authorids.concat(note.signatures),
      noninvitees: [],
      readers: ['everyone'],
      reply: {
        forum: note.id,
        referent: note.id,
        signatures: invitation.reply.signatures,
        writers: invitation.reply.writers,
        readers: invitation.reply.readers,
        content: invitation.reply.content
      }
    }

    var overwritingNote = {
      original: note.id,
      invitation: 'auai.org/UAI/2017/-/blind-submission',
      forum: null,
      parent: null,
      signatures: [CONFERENCE],
      writers: [CONFERENCE],
      readers: [CONFERENCE, COCHAIRS, SPC, PC],
      content: {
        authors: ['Blinded names'],
        authorids: ['Blinded names']
      }
    }

    //Send an email to the author of the submitted note, confirming its receipt
    var mail = {
        "groups": note.content.authorids,
        "subject": "Confirmation of your submission to UAI 2017: \"" + note.content.title + "\".",
        "message": `Your submission to UAI 2017 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
    };


    or3client.or3request(or3client.inviteUrl, referenceInvite, 'POST', token)
    .then(result => or3client.or3request(or3client.notesUrl, overwritingNote, 'POST', token))
    .then(savedNote => {
      var paperGroup = {
        id: CONFERENCE + '/Paper' + savedNote.number,
        signatures: [CONFERENCE],
        writers: [CONFERENCE],
        members: [],
        readers: ['everyone'],
        signatories: []
      };
      return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
      .then(savedPaperGroup => {
        var groupId = savedPaperGroup.id + '/Authors';
        var authorGroup = {
          id: groupId,
          signatures: [CONFERENCE],
          writers: [CONFERENCE],
          members: note.content.authorids.concat(note.signatures),
          readers: [COCHAIRS, groupId],
          signatories: [groupId]
        };
        return or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token)
        .then(savedGroup => {
          savedNote.content = {
            authorids: [savedGroup.id],
            authors: ['Blinded names']
          };
          savedNote.readers.push(savedGroup.id);
          return or3client.or3request(or3client.notesUrl, savedNote, 'POST', token);
        });
      });
    })
    .then(result => or3client.or3request(or3client.mailUrl, mail, 'POST', token))
    .then(result => done())
    .catch(error => done(error));

    return true;
}
