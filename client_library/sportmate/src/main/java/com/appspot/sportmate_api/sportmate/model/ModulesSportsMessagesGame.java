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
 * Message containing a game.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the sportmate. For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class ModulesSportsMessagesGame extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.util.List<java.lang.String> categories;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Double lat;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key @com.google.api.client.json.JsonString
  private java.lang.Long level;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Double lon;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.String name;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("players_full")
  private java.lang.Boolean playersFull;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("players_joined") @com.google.api.client.json.JsonString
  private java.lang.Long playersJoined;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("players_needed") @com.google.api.client.json.JsonString
  private java.lang.Long playersNeeded;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private com.google.api.client.util.DateTime time;

  /**
   * @return value or {@code null} for none
   */
  public java.util.List<java.lang.String> getCategories() {
    return categories;
  }

  /**
   * @param categories categories or {@code null} for none
   */
  public ModulesSportsMessagesGame setCategories(java.util.List<java.lang.String> categories) {
    this.categories = categories;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Double getLat() {
    return lat;
  }

  /**
   * @param lat lat or {@code null} for none
   */
  public ModulesSportsMessagesGame setLat(java.lang.Double lat) {
    this.lat = lat;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getLevel() {
    return level;
  }

  /**
   * @param level level or {@code null} for none
   */
  public ModulesSportsMessagesGame setLevel(java.lang.Long level) {
    this.level = level;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Double getLon() {
    return lon;
  }

  /**
   * @param lon lon or {@code null} for none
   */
  public ModulesSportsMessagesGame setLon(java.lang.Double lon) {
    this.lon = lon;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getName() {
    return name;
  }

  /**
   * @param name name or {@code null} for none
   */
  public ModulesSportsMessagesGame setName(java.lang.String name) {
    this.name = name;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Boolean getPlayersFull() {
    return playersFull;
  }

  /**
   * @param playersFull playersFull or {@code null} for none
   */
  public ModulesSportsMessagesGame setPlayersFull(java.lang.Boolean playersFull) {
    this.playersFull = playersFull;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getPlayersJoined() {
    return playersJoined;
  }

  /**
   * @param playersJoined playersJoined or {@code null} for none
   */
  public ModulesSportsMessagesGame setPlayersJoined(java.lang.Long playersJoined) {
    this.playersJoined = playersJoined;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getPlayersNeeded() {
    return playersNeeded;
  }

  /**
   * @param playersNeeded playersNeeded or {@code null} for none
   */
  public ModulesSportsMessagesGame setPlayersNeeded(java.lang.Long playersNeeded) {
    this.playersNeeded = playersNeeded;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public com.google.api.client.util.DateTime getTime() {
    return time;
  }

  /**
   * @param time time or {@code null} for none
   */
  public ModulesSportsMessagesGame setTime(com.google.api.client.util.DateTime time) {
    this.time = time;
    return this;
  }

  @Override
  public ModulesSportsMessagesGame set(String fieldName, Object value) {
    return (ModulesSportsMessagesGame) super.set(fieldName, value);
  }

  @Override
  public ModulesSportsMessagesGame clone() {
    return (ModulesSportsMessagesGame) super.clone();
  }

}
