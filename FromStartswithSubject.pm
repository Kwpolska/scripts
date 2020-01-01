# Copyright © 2018-2020, Chris Warrick. All rights reserved.
# License: 2-clause BSD
package FromStartswithSubject;
use Mail::SpamAssassin::Plugin;
our @ISA = qw(Mail::SpamAssassin::Plugin);
sub new {
    my ($class, $mailsa) = @_;

    # the usual perlobj boilerplate to create a subclass object
    $class = ref($class) || $class;
    my $self = $class->SUPER::new($mailsa);
    bless ($self, $class);

    # then register an eval rule, if desired...
    $self->register_eval_rule ("kw_from_startswith_subject");
    # and return the new plugin object
    return $self;
}

sub _trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };

sub kw_from_startswith_subject {
    my ($self, $permsgstatus) = @_;
    my $fr = $permsgstatus->get("From", "_F_null");
    my $su = $permsgstatus->get("Subject", "_S_null");
    my $qs = '"' . $su;
    if (length($su) > 10) {
        return 0;
    }
    # https://stackoverflow.com/questions/31724503/most-efficient-way-to-check-if-string-starts-with-needle-in-perl
    my $sub1 = substr($fr, 0, length($su) - 1);
    my $sub2 = substr($fr, 0, length($qs) - 1);
    if ((_trim($sub1) eq _trim($su)) || (_trim($sub2) eq _trim($qs))) {
        return 1;
    } else {
        return 0;
    }
}

1;
