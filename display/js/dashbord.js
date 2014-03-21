/*
   Copyright 2013 //SEIBERT/MEDIA GmbH https://www.seibert-media.net

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 
   Author: Ingmar Drewing <idrewing@seibert-media.net>
           Benjamin Peter <bpeter@seibert-media.net>

*/

$(function() {
  /* TODO Configure with an URL to the CI Dashboard that does not require any form
   * of authorization or SSL problems. */
  var DASHBOARD_BASE_URL                  = "https://example.com/dash";

  var errorMessageDisplayTimeMilliseconds = 19000;
  var refreshIntervalMilliseconds         = 20000;
  /* Defined by the space on your display */
  var maxLengthOfUsernameInChars          = 9;

  /* Is calculated by calculateMaxNumberOfDisplayedCommits() */
  var numberOfCommitsToDisplay            = undefined;
  /* Is calculated by determineDashboardURL() */
  var dashboard_url                       = undefined;

  var $globalBuildStatus                  = $("body");

  var $error = $("<div id='error'></div>");
  $("body").append($error);

  var $container = $("<div id='container'></div>");
  $("body").append($container);

  var statusSuccess   = "green";
  var statusFailure   = "red";
  var statusBuilding  = "building";
  var statusUnkown    = "gray";
  var statusSkipped   = "skipped";

  var STATUS_SUCCESS  = 3;
  var STATUS_FAILURE  = 2;
  var STATUS_BUILDING = 1;
  var STATUS_SKIPPED  = 99;

  function log(arg) {
    if (console && console.log) {
      console.log(arg);
    }
  }

  function _displayErrorMessage(msg) {
    var $errorMessage = $("<p>"+ msg +"</p>");
    $error.append($errorMessage);
    return $errorMessage;
  }

  function _removeErrorMessageAfterTime($errorMessage) {
    setTimeout(function() {
       $errorMessage.remove();
    }, errorMessageDisplayTimeMilliseconds);
  }

  function error(msg) {
    log("error: "+ msg);
    var $errorMessage = _displayErrorMessage(msg);
    _removeErrorMessageAfterTime($errorMessage);
  }

  function _determineDashboardURL(numberOfCommitsToDisplay) {
    return DASHBOARD_BASE_URL + '/bundle?branch=trunk&limit='+ numberOfCommitsToDisplay
      +'&sort=%5B%7B%22property%22%3A%22revision%22%2C%22direction%22%3A%22DESC%22%7D%5D';
  }

  function updateDashboardURL() {
    dashboard_url = _determineDashboardURL(numberOfCommitsToDisplay);
  }

  /* Converts the date in form '2013-07-11_16:41:55' to a String like "vor 23 min." */
  function jenkinsDateToText(jenkinsDate) {
    var now = new Date();
    var commitDate = parseJenkinsDate(jenkinsDate);
    return "vor "+ msToTime(now - commitDate);
  }

  /* Converts the date in form '2013-07-11_16:41:55' to a js Date object. */
  function parseJenkinsDate(jenkinsDate) {
    if (! jenkinsDate) { return new Date(0); }
    var parts = jenkinsDate.match(/\d+/g);
    if (parts === null) { return new Date(0); }
    parts[1] -= 1;
    return new Date(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]);
  }

  /* Converts a time difference in us to a string like "23 min." */
  function msToTime(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    s = (s - mins) / 60;
    var hrs = s % 24;
    s = (s - hrs) / 24;
    var days = s % 7;
    s = (s - days) / 7;
    var weeks = s % 30; /* about */
    s = (s - weeks) / 30;
   
    if (weeks == 1) {
      return "1 woche";
    }
    else if (weeks > 0) {
      return weeks + " wochen";
    }
    else if (days == 1) {
      return "1 tag"
    }
    else if (days > 1) {
      return days + " tagen"
    }
    else if (hrs == 1) {
      return "1 Std."
    }
    else if (hrs > 1) {
      return hrs + " Std."
    }
    else if (mins == 1) {
      return "1 Min."
    }
    else if (mins > 1) {
      return mins + " Min."
    }
    else if (secs == 1) {
      return "1 Sek."
    }
    else {
      return secs + " Sek."
    }
  }

  function isJenkinsStatusSuccess(jenkinsStatus) {
    return STATUS_SUCCESS == jenkinsStatus;
  }

  function isJenkinsStatusFailure(jenkinsStatus) {
    return STATUS_FAILURE == jenkinsStatus;
  }

  function isJenkinsStatusBuilding(jenkinsStatus) {
    return STATUS_BUILDING == jenkinsStatus;
  }

  function isJenkinsStatusSkipped(jenkinsStatus) {
    return STATUS_SKIPPED == jenkinsStatus;
  }

  function isJenkinsStatusUnkown(jenkinsStatus) {
    return ! (   isJenkinsStatusSuccess(jenkinsStatus)
              || isJenkinsStatusFailure(jenkinsStatus)
              || isJenkinsStatusBuilding(jenkinsStatus));
  }

  /* Converts a dashboard build status like 2 to a css class like
   * "red" or 3 to "green". */
  function jenkinsStatusToText(jenkinsStatus) {
    if (isJenkinsStatusSuccess(jenkinsStatus)) {
      return statusSuccess;
    }
    else if (isJenkinsStatusFailure(jenkinsStatus)) {
      return statusFailure;
    }
    else if (isJenkinsStatusBuilding(jenkinsStatus)) {
      return statusBuilding;
    }
    else if (isJenkinsStatusSkipped(jenkinsStatus)) {
      return statusSkipped;
    }
    else {
      return statusUnkown;
    }
  }

  /* Append a new commit line entry to the $container */
  function appendCommitLine(userId, commitDate, revisionNumber, statusStage1, statusStage2, statusStage3) {
    $container.append("<div class='commitLine'>"
      +"<div class='stagesContainer'>"
        +"<div class='stages " + statusStage1 + "'></div>"
        +"<div class='stages " + statusStage2 + "'></div>"
        +"<div class='stages animate " + statusStage3 + "'></div>"
      +"</div>"
      +"<div class='textWrapper'>"
        +"<div class='textContainer'>"
          + userId + "<span class='muted'> " + commitDate + "</span> " + revisionNumber 
        +"</div>"
      +"</div>"
    +"</div>");
  }

  function generateHeadline() {
    $container.append("<div class='commitLine'>"
      +"<div class='stagesContainer'>"
        +"<div class='stages '></div>"
        +"<div class='stages '></div>"
        +"<div class='stages '></div>"
      +"</div>"
      +"<div class='textWrapper headline'>"
        +"<div class='textHeadlineContainer'>Committer <span class='muted'>- Age of Commit - </span> Revision "
        +"</div>"
      +"</div>"
    +"</div>");
  }

  /* Adds an animation for building commits, currently disabled since
   * the raspberry pi had performance issues with it */
  function addAnimation() {
    var $c = $(".building");
    var fadeToTransparent = function($jqobjs) {
      $jqobjs.stop(true);
      $jqobjs.animate({opacity:0},1000,"linear",function() {
        fadeToOpaque($jqobjs);
      });
    };
    var fadeToOpaque = function($jqobjs) {
      $jqobjs.stop(true);
      $jqobjs.animate({opacity:1},1000,"linear",function() {
        fadeToTransparent($jqobjs);
     });
    };
    fadeToTransparent($c);
  }

  /* Looks at the window display size and calculates the
   * amount of commits that can be displayed */
  function _calculateMaxNumberOfDisplayedCommits() {
    /* The - 10 px are for padding */
    var h = $(window).height() - 10;
    var rowsize = 90;
    var returnValue = (h / rowsize) - 1;
    returnValue = Math.floor(returnValue);
    log("max number of diplayed commits: "+ returnValue);
    return returnValue;
  }

  function updateMaxNumberOfDisplayedCommits() {
    numberOfCommitsToDisplay = _calculateMaxNumberOfDisplayedCommits();
  }

  function isCommitFullyTested(commit) {
    return ! (isJenkinsStatusBuilding(commit.stage1) ||
              isJenkinsStatusBuilding(commit.stage2) ||
              isJenkinsStatusBuilding(commit.stage3));
  }

  /* Looks a the latest commit result and determines the
   * "global build status". The status is used to display a
   * colored background of the display.
   *
   * Rules are:
   * If at least one stage is failing, the status is: fail
   * If all stages are successful,     the status is: success
   * else,                             the status is: unknown
   */
  function determineGlobalBuildStatus(commits) {
    for (var i = 0; i < commits.length; i++) {
      commit = commits[i];
      if (! isCommitFullyTested(commit)) {
        continue;
      }

      /* all successfull */
      if (isJenkinsStatusSuccess(commit.stage1) &&
          isJenkinsStatusSuccess(commit.stage2) &&
          isJenkinsStatusSuccess(commit.stage3)) {
        return statusSuccess;
      }
      /* any failure */
      else if (isJenkinsStatusFailure(commit.stage1) ||
               isJenkinsStatusFailure(commit.stage2) ||
               isJenkinsStatusFailure(commit.stage3)) {
        return statusFailure;
      }
    }
    return statusUnkown;
  }

  /* Sets the background color according to the global build status */
  function updateGlobalBuildStatus(commits) {
    $globalBuildStatus.removeClass(statusSuccess);
    $globalBuildStatus.removeClass(statusFailure);
    $globalBuildStatus.removeClass(statusUnkown);
    $globalBuildStatus.addClass(determineGlobalBuildStatus(commits));
  }

  /* Refreshing commit list and scheduling the next update */
  function refreshCommitList() {
    updateMaxNumberOfDisplayedCommits();
    updateDashboardURL();

    log("refreshing display");
    $.get(dashboard_url, function(data_string, textStatus, jqXHR) {
      /*
       * {
       *  "id":"15.11132.1717"
       *  "branch":"trunk",
       *  "revision":"11132",
       *  "stage1":3,
       *  "stage2":3,
       *  "stage3":2,
       *  "timestamp":"2013-07-04_12:20:23",
       *  "committer":"jdoe"
       * },
       */
      log("got commit data response");
      try {
        var data = jQuery.parseJSON(data_string);
        if (data.success && data.results instanceof Array) {
          data.results.sort(compareTimeStamps);
          data.results.reverse();
          updateGlobalBuildStatus(data.results);
          updateCommitList(truncateCommitsList(data.results));
          scheduleRefreshCommitList();
        }
        else {
          error("Could not fetch commit list.");
          scheduleRefreshCommitList();
        }
      }
      catch (err) {
        /* This happens sometimes */
        log("Could not parse commit list: "+ err);
        scheduleRefreshCommitList();
      }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      error("Error fetching commit list: "+ errorThrown);
      scheduleRefreshCommitList();
    });
  }

  /* Sorting comparator, sort by timestamp */
  function compareTimeStamps(a,b) {
    if (! b) { return -1; }
    if (! a) { return 1; }
    return parseJenkinsDate(a.timestamp) - parseJenkinsDate(b.timestamp);
  }

  /* Truncate commit list by numberOfCommitsToDisplay */
  function truncateCommitsList(commits) {
    return commits.slice(0, numberOfCommitsToDisplay);
  }

  /* Truncate username by maxLengthOfUsernameInChars */
  function truncateUsername(username) {
    var chars = username.split("");
    if (chars.length > maxLengthOfUsernameInChars) {
      var charsOutput = chars.slice(0, maxLengthOfUsernameInChars);
      return charsOutput.join("") + "&hellip;";
    }
    return username;
  }

  function clearCommitList() {
    $container.empty();
  }

  function determineStatusStage1(commit) {
    return commit.stage1;
  }

  function determineStatusStage2(commit) {
    if (isJenkinsStatusFailure(commit.stage1)) {
      return STATUS_SKIPPED;
    }
    else {
      return commit.stage2;
    }
  }

  function determineStatusStage3(commit) {
    if (isJenkinsStatusFailure(commit.stage1) ||
        isJenkinsStatusFailure(commit.stage2)) {
      return STATUS_SKIPPED;
    }
    else {
      return commit.stage3;
    }
  }

  function updateCommitList(commits) {
    clearCommitList();

    jQuery.each(commits, function(index, commit) {
      if (index == 0) {
        generateHeadline();
      }

      appendCommitLine(
        truncateUsername(commit.committer),
        jenkinsDateToText(commit.timestamp),
        commit.revision,
        jenkinsStatusToText(determineStatusStage1(commit)),
        jenkinsStatusToText(determineStatusStage2(commit)),
        jenkinsStatusToText(determineStatusStage3(commit))
      );

      /* Animation deactivated because it used too much resources
       * on the raspberry pi
       * addAnimation();
       */
    });
  }

  function scheduleRefreshCommitList() {
    log("scheduling new page refresh")
    setTimeout(function() {
      refreshCommitList();
    }, refreshIntervalMilliseconds);
  }

  function init () {
    refreshCommitList();
  }

  init();
});

