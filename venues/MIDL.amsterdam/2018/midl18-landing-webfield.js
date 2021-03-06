var GROUP_ID = 'MIDL.amsterdam/2018';
var HEADER = {
  title: 'Medical Imaging with Deep Learning 2018',
  description: 'Welcome to OpenReview for MIDL 2018. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=MIDL.amsterdam/2018/Conference', name: 'MIDL 2018 Conference Track' },
  { url: '/group?id=MIDL.amsterdam/2018/Abstract', name: 'MIDL 2018 Abstract Track' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
