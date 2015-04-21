/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
/*
 * This code was generated by https://code.google.com/p/google-apis-client-generator/
 * (build: 2015-03-26 20:30:19 UTC)
 * on 2015-04-21 at 17:28:59 UTC 
 * Modify at your own risk.
 */

package com.appspot.sportmate_api.sportmate.model;

/**
 * Message about a relationship between two users.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the sportmate. For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class UsersMessagesRelationship extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("friend_request_rejected")
  private java.lang.Boolean friendRequestRejected;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("friend_request_sender_id") @com.google.api.client.json.JsonString
  private java.lang.Long friendRequestSenderId;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("friend_request_sent")
  private java.lang.Boolean friendRequestSent;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("friend_unfriender_id") @com.google.api.client.json.JsonString
  private java.lang.Long friendUnfrienderId;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("is_friends")
  private java.lang.Boolean isFriends;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.util.List<java.lang.Long> users;

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Boolean getFriendRequestRejected() {
    return friendRequestRejected;
  }

  /**
   * @param friendRequestRejected friendRequestRejected or {@code null} for none
   */
  public UsersMessagesRelationship setFriendRequestRejected(java.lang.Boolean friendRequestRejected) {
    this.friendRequestRejected = friendRequestRejected;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getFriendRequestSenderId() {
    return friendRequestSenderId;
  }

  /**
   * @param friendRequestSenderId friendRequestSenderId or {@code null} for none
   */
  public UsersMessagesRelationship setFriendRequestSenderId(java.lang.Long friendRequestSenderId) {
    this.friendRequestSenderId = friendRequestSenderId;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Boolean getFriendRequestSent() {
    return friendRequestSent;
  }

  /**
   * @param friendRequestSent friendRequestSent or {@code null} for none
   */
  public UsersMessagesRelationship setFriendRequestSent(java.lang.Boolean friendRequestSent) {
    this.friendRequestSent = friendRequestSent;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getFriendUnfrienderId() {
    return friendUnfrienderId;
  }

  /**
   * @param friendUnfrienderId friendUnfrienderId or {@code null} for none
   */
  public UsersMessagesRelationship setFriendUnfrienderId(java.lang.Long friendUnfrienderId) {
    this.friendUnfrienderId = friendUnfrienderId;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Boolean getIsFriends() {
    return isFriends;
  }

  /**
   * @param isFriends isFriends or {@code null} for none
   */
  public UsersMessagesRelationship setIsFriends(java.lang.Boolean isFriends) {
    this.isFriends = isFriends;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.util.List<java.lang.Long> getUsers() {
    return users;
  }

  /**
   * @param users users or {@code null} for none
   */
  public UsersMessagesRelationship setUsers(java.util.List<java.lang.Long> users) {
    this.users = users;
    return this;
  }

  @Override
  public UsersMessagesRelationship set(String fieldName, Object value) {
    return (UsersMessagesRelationship) super.set(fieldName, value);
  }

  @Override
  public UsersMessagesRelationship clone() {
    return (UsersMessagesRelationship) super.clone();
  }

}