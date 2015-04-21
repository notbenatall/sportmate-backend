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
 * on 2015-04-21 at 13:59:34 UTC 
 * Modify at your own risk.
 */

package com.appspot.sportmate_api.sportmate;

/**
 * Service definition for Sportmate (v1.0).
 *
 * <p>
 * This is an API
 * </p>
 *
 * <p>
 * For more information about this service, see the
 * <a href="" target="_blank">API Documentation</a>
 * </p>
 *
 * <p>
 * This service uses {@link SportmateRequestInitializer} to initialize global parameters via its
 * {@link Builder}.
 * </p>
 *
 * @since 1.3
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public class Sportmate extends com.google.api.client.googleapis.services.json.AbstractGoogleJsonClient {

  // Note: Leave this static initializer at the top of the file.
  static {
    com.google.api.client.util.Preconditions.checkState(
        com.google.api.client.googleapis.GoogleUtils.MAJOR_VERSION == 1 &&
        com.google.api.client.googleapis.GoogleUtils.MINOR_VERSION >= 15,
        "You are currently running with version %s of google-api-client. " +
        "You need at least version 1.15 of google-api-client to run version " +
        "1.20.0 of the sportmate library.", com.google.api.client.googleapis.GoogleUtils.VERSION);
  }

  /**
   * The default encoded root URL of the service. This is determined when the library is generated
   * and normally should not be changed.
   *
   * @since 1.7
   */
  public static final String DEFAULT_ROOT_URL = "https://sportmate_api.appspot.com/_ah/api/";

  /**
   * The default encoded service path of the service. This is determined when the library is
   * generated and normally should not be changed.
   *
   * @since 1.7
   */
  public static final String DEFAULT_SERVICE_PATH = "sportmate/v1.0/";

  /**
   * The default encoded base URL of the service. This is determined when the library is generated
   * and normally should not be changed.
   */
  public static final String DEFAULT_BASE_URL = DEFAULT_ROOT_URL + DEFAULT_SERVICE_PATH;

  /**
   * Constructor.
   *
   * <p>
   * Use {@link Builder} if you need to specify any of the optional parameters.
   * </p>
   *
   * @param transport HTTP transport, which should normally be:
   *        <ul>
   *        <li>Google App Engine:
   *        {@code com.google.api.client.extensions.appengine.http.UrlFetchTransport}</li>
   *        <li>Android: {@code newCompatibleTransport} from
   *        {@code com.google.api.client.extensions.android.http.AndroidHttp}</li>
   *        <li>Java: {@link com.google.api.client.googleapis.javanet.GoogleNetHttpTransport#newTrustedTransport()}
   *        </li>
   *        </ul>
   * @param jsonFactory JSON factory, which may be:
   *        <ul>
   *        <li>Jackson: {@code com.google.api.client.json.jackson2.JacksonFactory}</li>
   *        <li>Google GSON: {@code com.google.api.client.json.gson.GsonFactory}</li>
   *        <li>Android Honeycomb or higher:
   *        {@code com.google.api.client.extensions.android.json.AndroidJsonFactory}</li>
   *        </ul>
   * @param httpRequestInitializer HTTP request initializer or {@code null} for none
   * @since 1.7
   */
  public Sportmate(com.google.api.client.http.HttpTransport transport, com.google.api.client.json.JsonFactory jsonFactory,
      com.google.api.client.http.HttpRequestInitializer httpRequestInitializer) {
    this(new Builder(transport, jsonFactory, httpRequestInitializer));
  }

  /**
   * @param builder builder
   */
  Sportmate(Builder builder) {
    super(builder);
  }

  @Override
  protected void initialize(com.google.api.client.googleapis.services.AbstractGoogleClientRequest<?> httpClientRequest) throws java.io.IOException {
    super.initialize(httpClientRequest);
  }

  /**
   * An accessor for creating requests from the Facebook collection.
   *
   * <p>The typical use is:</p>
   * <pre>
   *   {@code Sportmate sportmate = new Sportmate(...);}
   *   {@code Sportmate.Facebook.List request = sportmate.facebook().list(parameters ...)}
   * </pre>
   *
   * @return the resource collection
   */
  public Facebook facebook() {
    return new Facebook();
  }

  /**
   * The "facebook" collection of methods.
   */
  public class Facebook {

    /**
     * An accessor for creating requests from the Login collection.
     *
     * <p>The typical use is:</p>
     * <pre>
     *   {@code Sportmate sportmate = new Sportmate(...);}
     *   {@code Sportmate.Login.List request = sportmate.login().list(parameters ...)}
     * </pre>
     *
     * @return the resource collection
     */
    public Login login() {
      return new Login();
    }

    /**
     * The "login" collection of methods.
     */
    public class Login {

      /**
       * Returns the Facebook login URL.
       *
       * Create a request for the method "login.geturl".
       *
       * This request holds the parameters needed by the sportmate server.  After setting any optional
       * parameters, call the {@link Geturl#execute()} method to invoke the remote operation.
       *
       * @return the request
       */
      public Geturl geturl() throws java.io.IOException {
        Geturl result = new Geturl();
        initialize(result);
        return result;
      }

      public class Geturl extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.ModulesFacebookMessagesUrl> {

        private static final String REST_PATH = "geturl";

        /**
         * Returns the Facebook login URL.
         *
         * Create a request for the method "login.geturl".
         *
         * This request holds the parameters needed by the the sportmate server.  After setting any
         * optional parameters, call the {@link Geturl#execute()} method to invoke the remote operation.
         * <p> {@link
         * Geturl#initialize(com.google.api.client.googleapis.services.AbstractGoogleClientRequest)} must
         * be called to initialize this instance immediately after invoking the constructor. </p>
         *
         * @since 1.13
         */
        protected Geturl() {
          super(Sportmate.this, "GET", REST_PATH, null, com.appspot.sportmate_api.sportmate.model.ModulesFacebookMessagesUrl.class);
        }

        @Override
        public com.google.api.client.http.HttpResponse executeUsingHead() throws java.io.IOException {
          return super.executeUsingHead();
        }

        @Override
        public com.google.api.client.http.HttpRequest buildHttpRequestUsingHead() throws java.io.IOException {
          return super.buildHttpRequestUsingHead();
        }

        @Override
        public Geturl setAlt(java.lang.String alt) {
          return (Geturl) super.setAlt(alt);
        }

        @Override
        public Geturl setFields(java.lang.String fields) {
          return (Geturl) super.setFields(fields);
        }

        @Override
        public Geturl setKey(java.lang.String key) {
          return (Geturl) super.setKey(key);
        }

        @Override
        public Geturl setOauthToken(java.lang.String oauthToken) {
          return (Geturl) super.setOauthToken(oauthToken);
        }

        @Override
        public Geturl setPrettyPrint(java.lang.Boolean prettyPrint) {
          return (Geturl) super.setPrettyPrint(prettyPrint);
        }

        @Override
        public Geturl setQuotaUser(java.lang.String quotaUser) {
          return (Geturl) super.setQuotaUser(quotaUser);
        }

        @Override
        public Geturl setUserIp(java.lang.String userIp) {
          return (Geturl) super.setUserIp(userIp);
        }

        @Override
        public Geturl set(String parameterName, Object value) {
          return (Geturl) super.set(parameterName, value);
        }
      }
      /**
       * Uses the login code provided by Facebook and logs in the user.
       *
       * Create a request for the method "login.recieve_code".
       *
       * This request holds the parameters needed by the sportmate server.  After setting any optional
       * parameters, call the {@link RecieveCode#execute()} method to invoke the remote operation.
       *
       * @return the request
       */
      public RecieveCode recieveCode() throws java.io.IOException {
        RecieveCode result = new RecieveCode();
        initialize(result);
        return result;
      }

      public class RecieveCode extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.ModulesFacebookMessagesFacebookAccountWithUser> {

        private static final String REST_PATH = "code";

        /**
         * Uses the login code provided by Facebook and logs in the user.
         *
         * Create a request for the method "login.recieve_code".
         *
         * This request holds the parameters needed by the the sportmate server.  After setting any
         * optional parameters, call the {@link RecieveCode#execute()} method to invoke the remote
         * operation. <p> {@link
         * RecieveCode#initialize(com.google.api.client.googleapis.services.AbstractGoogleClientRequest)}
         * must be called to initialize this instance immediately after invoking the constructor. </p>
         *
         * @since 1.13
         */
        protected RecieveCode() {
          super(Sportmate.this, "GET", REST_PATH, null, com.appspot.sportmate_api.sportmate.model.ModulesFacebookMessagesFacebookAccountWithUser.class);
        }

        @Override
        public com.google.api.client.http.HttpResponse executeUsingHead() throws java.io.IOException {
          return super.executeUsingHead();
        }

        @Override
        public com.google.api.client.http.HttpRequest buildHttpRequestUsingHead() throws java.io.IOException {
          return super.buildHttpRequestUsingHead();
        }

        @Override
        public RecieveCode setAlt(java.lang.String alt) {
          return (RecieveCode) super.setAlt(alt);
        }

        @Override
        public RecieveCode setFields(java.lang.String fields) {
          return (RecieveCode) super.setFields(fields);
        }

        @Override
        public RecieveCode setKey(java.lang.String key) {
          return (RecieveCode) super.setKey(key);
        }

        @Override
        public RecieveCode setOauthToken(java.lang.String oauthToken) {
          return (RecieveCode) super.setOauthToken(oauthToken);
        }

        @Override
        public RecieveCode setPrettyPrint(java.lang.Boolean prettyPrint) {
          return (RecieveCode) super.setPrettyPrint(prettyPrint);
        }

        @Override
        public RecieveCode setQuotaUser(java.lang.String quotaUser) {
          return (RecieveCode) super.setQuotaUser(quotaUser);
        }

        @Override
        public RecieveCode setUserIp(java.lang.String userIp) {
          return (RecieveCode) super.setUserIp(userIp);
        }

        @com.google.api.client.util.Key
        private java.lang.String code;

        /**

         */
        public java.lang.String getCode() {
          return code;
        }

        public RecieveCode setCode(java.lang.String code) {
          this.code = code;
          return this;
        }

        @Override
        public RecieveCode set(String parameterName, Object value) {
          return (RecieveCode) super.set(parameterName, value);
        }
      }

    }
  }

  /**
   * An accessor for creating requests from the Sports collection.
   *
   * <p>The typical use is:</p>
   * <pre>
   *   {@code Sportmate sportmate = new Sportmate(...);}
   *   {@code Sportmate.Sports.List request = sportmate.sports().list(parameters ...)}
   * </pre>
   *
   * @return the resource collection
   */
  public Sports sports() {
    return new Sports();
  }

  /**
   * The "sports" collection of methods.
   */
  public class Sports {

    /**
     * Adds a new game to the system.
     *
     * Create a request for the method "sports.creategame".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Creategame#execute()} method to invoke the remote operation.
     *
     * @param content the {@link com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesNewGame}
     * @return the request
     */
    public Creategame creategame(com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesNewGame content) throws java.io.IOException {
      Creategame result = new Creategame(content);
      initialize(result);
      return result;
    }

    public class Creategame extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesGame> {

      private static final String REST_PATH = "create";

      /**
       * Adds a new game to the system.
       *
       * Create a request for the method "sports.creategame".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Creategame#execute()} method to invoke the remote
       * operation. <p> {@link
       * Creategame#initialize(com.google.api.client.googleapis.services.AbstractGoogleClientRequest)}
       * must be called to initialize this instance immediately after invoking the constructor. </p>
       *
       * @param content the {@link com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesNewGame}
       * @since 1.13
       */
      protected Creategame(com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesNewGame content) {
        super(Sportmate.this, "POST", REST_PATH, content, com.appspot.sportmate_api.sportmate.model.ModulesSportsMessagesGame.class);
      }

      @Override
      public Creategame setAlt(java.lang.String alt) {
        return (Creategame) super.setAlt(alt);
      }

      @Override
      public Creategame setFields(java.lang.String fields) {
        return (Creategame) super.setFields(fields);
      }

      @Override
      public Creategame setKey(java.lang.String key) {
        return (Creategame) super.setKey(key);
      }

      @Override
      public Creategame setOauthToken(java.lang.String oauthToken) {
        return (Creategame) super.setOauthToken(oauthToken);
      }

      @Override
      public Creategame setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Creategame) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Creategame setQuotaUser(java.lang.String quotaUser) {
        return (Creategame) super.setQuotaUser(quotaUser);
      }

      @Override
      public Creategame setUserIp(java.lang.String userIp) {
        return (Creategame) super.setUserIp(userIp);
      }

      @Override
      public Creategame set(String parameterName, Object value) {
        return (Creategame) super.set(parameterName, value);
      }
    }

  }

  /**
   * An accessor for creating requests from the Users collection.
   *
   * <p>The typical use is:</p>
   * <pre>
   *   {@code Sportmate sportmate = new Sportmate(...);}
   *   {@code Sportmate.Users.List request = sportmate.users().list(parameters ...)}
   * </pre>
   *
   * @return the resource collection
   */
  public Users users() {
    return new Users();
  }

  /**
   * The "users" collection of methods.
   */
  public class Users {

    /**
     * Return a list of friends for the specified user.
     *
     * Create a request for the method "users.friendlist".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Friendlist#execute()} method to invoke the remote operation.
     *
     * @return the request
     */
    public Friendlist friendlist() throws java.io.IOException {
      Friendlist result = new Friendlist();
      initialize(result);
      return result;
    }

    public class Friendlist extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendList> {

      private static final String REST_PATH = "friend/list";

      /**
       * Return a list of friends for the specified user.
       *
       * Create a request for the method "users.friendlist".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Friendlist#execute()} method to invoke the remote
       * operation. <p> {@link
       * Friendlist#initialize(com.google.api.client.googleapis.services.AbstractGoogleClientRequest)}
       * must be called to initialize this instance immediately after invoking the constructor. </p>
       *
       * @since 1.13
       */
      protected Friendlist() {
        super(Sportmate.this, "GET", REST_PATH, null, com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendList.class);
      }

      @Override
      public com.google.api.client.http.HttpResponse executeUsingHead() throws java.io.IOException {
        return super.executeUsingHead();
      }

      @Override
      public com.google.api.client.http.HttpRequest buildHttpRequestUsingHead() throws java.io.IOException {
        return super.buildHttpRequestUsingHead();
      }

      @Override
      public Friendlist setAlt(java.lang.String alt) {
        return (Friendlist) super.setAlt(alt);
      }

      @Override
      public Friendlist setFields(java.lang.String fields) {
        return (Friendlist) super.setFields(fields);
      }

      @Override
      public Friendlist setKey(java.lang.String key) {
        return (Friendlist) super.setKey(key);
      }

      @Override
      public Friendlist setOauthToken(java.lang.String oauthToken) {
        return (Friendlist) super.setOauthToken(oauthToken);
      }

      @Override
      public Friendlist setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Friendlist) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Friendlist setQuotaUser(java.lang.String quotaUser) {
        return (Friendlist) super.setQuotaUser(quotaUser);
      }

      @Override
      public Friendlist setUserIp(java.lang.String userIp) {
        return (Friendlist) super.setUserIp(userIp);
      }

      @com.google.api.client.util.Key
      private java.lang.String token;

      /**

       */
      public java.lang.String getToken() {
        return token;
      }

      public Friendlist setToken(java.lang.String token) {
        this.token = token;
        return this;
      }

      @com.google.api.client.util.Key
      private java.lang.Long user;

      /**

       */
      public java.lang.Long getUser() {
        return user;
      }

      public Friendlist setUser(java.lang.Long user) {
        this.user = user;
        return this;
      }

      @Override
      public Friendlist set(String parameterName, Object value) {
        return (Friendlist) super.set(parameterName, value);
      }
    }
    /**
     * Send a friend request.
     *
     * Create a request for the method "users.friendrequest".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Friendrequest#execute()} method to invoke the remote operation.
     *
     * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId}
     * @return the request
     */
    public Friendrequest friendrequest(com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId content) throws java.io.IOException {
      Friendrequest result = new Friendrequest(content);
      initialize(result);
      return result;
    }

    public class Friendrequest extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship> {

      private static final String REST_PATH = "friend/request";

      /**
       * Send a friend request.
       *
       * Create a request for the method "users.friendrequest".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Friendrequest#execute()} method to invoke the remote
       * operation. <p> {@link Friendrequest#initialize(com.google.api.client.googleapis.services.Abstra
       * ctGoogleClientRequest)} must be called to initialize this instance immediately after invoking
       * the constructor. </p>
       *
       * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId}
       * @since 1.13
       */
      protected Friendrequest(com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId content) {
        super(Sportmate.this, "POST", REST_PATH, content, com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship.class);
      }

      @Override
      public Friendrequest setAlt(java.lang.String alt) {
        return (Friendrequest) super.setAlt(alt);
      }

      @Override
      public Friendrequest setFields(java.lang.String fields) {
        return (Friendrequest) super.setFields(fields);
      }

      @Override
      public Friendrequest setKey(java.lang.String key) {
        return (Friendrequest) super.setKey(key);
      }

      @Override
      public Friendrequest setOauthToken(java.lang.String oauthToken) {
        return (Friendrequest) super.setOauthToken(oauthToken);
      }

      @Override
      public Friendrequest setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Friendrequest) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Friendrequest setQuotaUser(java.lang.String quotaUser) {
        return (Friendrequest) super.setQuotaUser(quotaUser);
      }

      @Override
      public Friendrequest setUserIp(java.lang.String userIp) {
        return (Friendrequest) super.setUserIp(userIp);
      }

      @Override
      public Friendrequest set(String parameterName, Object value) {
        return (Friendrequest) super.set(parameterName, value);
      }
    }
    /**
     * Remove the specified user as a friend of the authenticating user.
     *
     * Create a request for the method "users.friendunfriend".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Friendunfriend#execute()} method to invoke the remote operation.
     *
     * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId}
     * @return the request
     */
    public Friendunfriend friendunfriend(com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId content) throws java.io.IOException {
      Friendunfriend result = new Friendunfriend(content);
      initialize(result);
      return result;
    }

    public class Friendunfriend extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship> {

      private static final String REST_PATH = "friend/unfriend";

      /**
       * Remove the specified user as a friend of the authenticating user.
       *
       * Create a request for the method "users.friendunfriend".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Friendunfriend#execute()} method to invoke the remote
       * operation. <p> {@link Friendunfriend#initialize(com.google.api.client.googleapis.services.Abstr
       * actGoogleClientRequest)} must be called to initialize this instance immediately after invoking
       * the constructor. </p>
       *
       * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId}
       * @since 1.13
       */
      protected Friendunfriend(com.appspot.sportmate_api.sportmate.model.UsersMessagesUserId content) {
        super(Sportmate.this, "POST", REST_PATH, content, com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship.class);
      }

      @Override
      public Friendunfriend setAlt(java.lang.String alt) {
        return (Friendunfriend) super.setAlt(alt);
      }

      @Override
      public Friendunfriend setFields(java.lang.String fields) {
        return (Friendunfriend) super.setFields(fields);
      }

      @Override
      public Friendunfriend setKey(java.lang.String key) {
        return (Friendunfriend) super.setKey(key);
      }

      @Override
      public Friendunfriend setOauthToken(java.lang.String oauthToken) {
        return (Friendunfriend) super.setOauthToken(oauthToken);
      }

      @Override
      public Friendunfriend setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Friendunfriend) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Friendunfriend setQuotaUser(java.lang.String quotaUser) {
        return (Friendunfriend) super.setQuotaUser(quotaUser);
      }

      @Override
      public Friendunfriend setUserIp(java.lang.String userIp) {
        return (Friendunfriend) super.setUserIp(userIp);
      }

      @Override
      public Friendunfriend set(String parameterName, Object value) {
        return (Friendunfriend) super.set(parameterName, value);
      }
    }
    /**
     * Answer a friend request from a user to the authenticating user.
     *
     * Create a request for the method "users.requestresponse".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Requestresponse#execute()} method to invoke the remote operation.
     *
     * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendRequestResponse}
     * @return the request
     */
    public Requestresponse requestresponse(com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendRequestResponse content) throws java.io.IOException {
      Requestresponse result = new Requestresponse(content);
      initialize(result);
      return result;
    }

    public class Requestresponse extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship> {

      private static final String REST_PATH = "friend/request/response";

      /**
       * Answer a friend request from a user to the authenticating user.
       *
       * Create a request for the method "users.requestresponse".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Requestresponse#execute()} method to invoke the remote
       * operation. <p> {@link Requestresponse#initialize(com.google.api.client.googleapis.services.Abst
       * ractGoogleClientRequest)} must be called to initialize this instance immediately after invoking
       * the constructor. </p>
       *
       * @param content the {@link com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendRequestResponse}
       * @since 1.13
       */
      protected Requestresponse(com.appspot.sportmate_api.sportmate.model.UsersMessagesFriendRequestResponse content) {
        super(Sportmate.this, "POST", REST_PATH, content, com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship.class);
      }

      @Override
      public Requestresponse setAlt(java.lang.String alt) {
        return (Requestresponse) super.setAlt(alt);
      }

      @Override
      public Requestresponse setFields(java.lang.String fields) {
        return (Requestresponse) super.setFields(fields);
      }

      @Override
      public Requestresponse setKey(java.lang.String key) {
        return (Requestresponse) super.setKey(key);
      }

      @Override
      public Requestresponse setOauthToken(java.lang.String oauthToken) {
        return (Requestresponse) super.setOauthToken(oauthToken);
      }

      @Override
      public Requestresponse setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Requestresponse) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Requestresponse setQuotaUser(java.lang.String quotaUser) {
        return (Requestresponse) super.setQuotaUser(quotaUser);
      }

      @Override
      public Requestresponse setUserIp(java.lang.String userIp) {
        return (Requestresponse) super.setUserIp(userIp);
      }

      @Override
      public Requestresponse set(String parameterName, Object value) {
        return (Requestresponse) super.set(parameterName, value);
      }
    }
    /**
     * Returns the relationship between two users.
     *
     * Create a request for the method "users.userrelationship".
     *
     * This request holds the parameters needed by the sportmate server.  After setting any optional
     * parameters, call the {@link Userrelationship#execute()} method to invoke the remote operation.
     *
     * @return the request
     */
    public Userrelationship userrelationship() throws java.io.IOException {
      Userrelationship result = new Userrelationship();
      initialize(result);
      return result;
    }

    public class Userrelationship extends SportmateRequest<com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship> {

      private static final String REST_PATH = "user/relationship";

      /**
       * Returns the relationship between two users.
       *
       * Create a request for the method "users.userrelationship".
       *
       * This request holds the parameters needed by the the sportmate server.  After setting any
       * optional parameters, call the {@link Userrelationship#execute()} method to invoke the remote
       * operation. <p> {@link Userrelationship#initialize(com.google.api.client.googleapis.services.Abs
       * tractGoogleClientRequest)} must be called to initialize this instance immediately after
       * invoking the constructor. </p>
       *
       * @since 1.13
       */
      protected Userrelationship() {
        super(Sportmate.this, "GET", REST_PATH, null, com.appspot.sportmate_api.sportmate.model.UsersMessagesRelationship.class);
      }

      @Override
      public com.google.api.client.http.HttpResponse executeUsingHead() throws java.io.IOException {
        return super.executeUsingHead();
      }

      @Override
      public com.google.api.client.http.HttpRequest buildHttpRequestUsingHead() throws java.io.IOException {
        return super.buildHttpRequestUsingHead();
      }

      @Override
      public Userrelationship setAlt(java.lang.String alt) {
        return (Userrelationship) super.setAlt(alt);
      }

      @Override
      public Userrelationship setFields(java.lang.String fields) {
        return (Userrelationship) super.setFields(fields);
      }

      @Override
      public Userrelationship setKey(java.lang.String key) {
        return (Userrelationship) super.setKey(key);
      }

      @Override
      public Userrelationship setOauthToken(java.lang.String oauthToken) {
        return (Userrelationship) super.setOauthToken(oauthToken);
      }

      @Override
      public Userrelationship setPrettyPrint(java.lang.Boolean prettyPrint) {
        return (Userrelationship) super.setPrettyPrint(prettyPrint);
      }

      @Override
      public Userrelationship setQuotaUser(java.lang.String quotaUser) {
        return (Userrelationship) super.setQuotaUser(quotaUser);
      }

      @Override
      public Userrelationship setUserIp(java.lang.String userIp) {
        return (Userrelationship) super.setUserIp(userIp);
      }

      @com.google.api.client.util.Key
      private java.lang.String token;

      /**

       */
      public java.lang.String getToken() {
        return token;
      }

      public Userrelationship setToken(java.lang.String token) {
        this.token = token;
        return this;
      }

      @com.google.api.client.util.Key
      private java.lang.Long userB;

      /**

       */
      public java.lang.Long getUserB() {
        return userB;
      }

      public Userrelationship setUserB(java.lang.Long userB) {
        this.userB = userB;
        return this;
      }

      @com.google.api.client.util.Key
      private java.lang.Long userA;

      /**

       */
      public java.lang.Long getUserA() {
        return userA;
      }

      public Userrelationship setUserA(java.lang.Long userA) {
        this.userA = userA;
        return this;
      }

      @Override
      public Userrelationship set(String parameterName, Object value) {
        return (Userrelationship) super.set(parameterName, value);
      }
    }

  }

  /**
   * Builder for {@link Sportmate}.
   *
   * <p>
   * Implementation is not thread-safe.
   * </p>
   *
   * @since 1.3.0
   */
  public static final class Builder extends com.google.api.client.googleapis.services.json.AbstractGoogleJsonClient.Builder {

    /**
     * Returns an instance of a new builder.
     *
     * @param transport HTTP transport, which should normally be:
     *        <ul>
     *        <li>Google App Engine:
     *        {@code com.google.api.client.extensions.appengine.http.UrlFetchTransport}</li>
     *        <li>Android: {@code newCompatibleTransport} from
     *        {@code com.google.api.client.extensions.android.http.AndroidHttp}</li>
     *        <li>Java: {@link com.google.api.client.googleapis.javanet.GoogleNetHttpTransport#newTrustedTransport()}
     *        </li>
     *        </ul>
     * @param jsonFactory JSON factory, which may be:
     *        <ul>
     *        <li>Jackson: {@code com.google.api.client.json.jackson2.JacksonFactory}</li>
     *        <li>Google GSON: {@code com.google.api.client.json.gson.GsonFactory}</li>
     *        <li>Android Honeycomb or higher:
     *        {@code com.google.api.client.extensions.android.json.AndroidJsonFactory}</li>
     *        </ul>
     * @param httpRequestInitializer HTTP request initializer or {@code null} for none
     * @since 1.7
     */
    public Builder(com.google.api.client.http.HttpTransport transport, com.google.api.client.json.JsonFactory jsonFactory,
        com.google.api.client.http.HttpRequestInitializer httpRequestInitializer) {
      super(
          transport,
          jsonFactory,
          DEFAULT_ROOT_URL,
          DEFAULT_SERVICE_PATH,
          httpRequestInitializer,
          false);
    }

    /** Builds a new instance of {@link Sportmate}. */
    @Override
    public Sportmate build() {
      return new Sportmate(this);
    }

    @Override
    public Builder setRootUrl(String rootUrl) {
      return (Builder) super.setRootUrl(rootUrl);
    }

    @Override
    public Builder setServicePath(String servicePath) {
      return (Builder) super.setServicePath(servicePath);
    }

    @Override
    public Builder setHttpRequestInitializer(com.google.api.client.http.HttpRequestInitializer httpRequestInitializer) {
      return (Builder) super.setHttpRequestInitializer(httpRequestInitializer);
    }

    @Override
    public Builder setApplicationName(String applicationName) {
      return (Builder) super.setApplicationName(applicationName);
    }

    @Override
    public Builder setSuppressPatternChecks(boolean suppressPatternChecks) {
      return (Builder) super.setSuppressPatternChecks(suppressPatternChecks);
    }

    @Override
    public Builder setSuppressRequiredParameterChecks(boolean suppressRequiredParameterChecks) {
      return (Builder) super.setSuppressRequiredParameterChecks(suppressRequiredParameterChecks);
    }

    @Override
    public Builder setSuppressAllChecks(boolean suppressAllChecks) {
      return (Builder) super.setSuppressAllChecks(suppressAllChecks);
    }

    /**
     * Set the {@link SportmateRequestInitializer}.
     *
     * @since 1.12
     */
    public Builder setSportmateRequestInitializer(
        SportmateRequestInitializer sportmateRequestInitializer) {
      return (Builder) super.setGoogleClientRequestInitializer(sportmateRequestInitializer);
    }

    @Override
    public Builder setGoogleClientRequestInitializer(
        com.google.api.client.googleapis.services.GoogleClientRequestInitializer googleClientRequestInitializer) {
      return (Builder) super.setGoogleClientRequestInitializer(googleClientRequestInitializer);
    }
  }
}
