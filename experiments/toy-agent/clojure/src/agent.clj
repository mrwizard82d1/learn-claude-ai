;; A toy coding agent in Clojure, talking to the raw HTTP API (no SDK).
;;
;; The loop is `run`, a tail-recursive function over the growing message vector:
;; call the model, run any tools it asks for, conj the results on, and `recur`
;; until it stops asking. Because clj-http parses the JSON into Clojure data and
;; cheshire serializes it back, echoing the assistant turn is just (:content response).

(ns agent
  (:require [clj-http.client :as http]
            [cheshire.core :as json]
            [clojure.java.io :as io]
            [clojure.string :as string]))

(def model "claude-opus-4-8")
(def url "https://api.anthropic.com/v1/messages")
(def api-key (System/getenv "ANTHROPIC_API_KEY"))

;; --- Tool definitions: the only things the agent can do in the world ---------
(def tools
  [{:name "list_files"
    :description (str "List the files and directories in a directory. "
                      "Call this to explore the codebase before reading files.")
    :input_schema {:type "object"
                   :properties {:directory {:type "string"
                                            :description "Directory to list. Defaults to the current directory."}}}}
   {:name "read_file"
    :description (str "Read the full contents of a file. Call this when you "
                      "need to see what is inside a specific file.")
    :input_schema {:type "object"
                   :properties {:path {:type "string" :description "Path to the file to read."}}
                   :required ["path"]}}])

;; --- Tool implementations ----------------------------------------------------
(defn execute-tool [name input]
  (try
    (case name
      "list_files" (->> (.listFiles (io/file (get input :directory ".")))
                        (map #(.getName %))
                        sort
                        (string/join "\n"))
      "read_file"  (slurp (:path input))
      (str "error: unknown tool " name))
    (catch Exception e (str "error: " (.getMessage e)))))

;; --- One round trip to the API -----------------------------------------------
(defn call-api [messages]
  (:body (http/post url
                    {:headers {"x-api-key" api-key
                               "anthropic-version" "2023-06-01"}
                     :content-type :json
                     :as :json
                     :body (json/generate-string {:model model
                                                  :max_tokens 16000
                                                  :tools tools
                                                  :messages messages})})))

;; --- The loop ----------------------------------------------------------------
(defn run [messages]
  (let [response  (call-api messages)
        content   (:content response)
        ;; Echo the assistant turn back into history verbatim.
        messages  (conj messages {:role "assistant" :content content})
        tool-uses (filter #(= "tool_use" (:type %)) content)]
    (if (empty? tool-uses)
      (do (doseq [b content]
            (when (= "text" (:type b)) (println (:text b))))
          messages)
      (let [results  (mapv (fn [tu]
                             {:type "tool_result"
                              :tool_use_id (:id tu)
                              :content (execute-tool (:name tu) (:input tu))})
                           tool-uses)
            messages (conj messages {:role "user" :content results})]
        (recur messages)))))

(defn -main [& _]
  (println "Toy agent. Ask about files in this directory. Ctrl-D to quit.")
  (loop [messages []]
    (print "you> ") (flush)
    (when-let [line (read-line)]
      (recur (run (conj messages {:role "user" :content line}))))))
