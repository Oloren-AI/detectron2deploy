import os
import io
import json
import modal

stub = modal.Stub("run-detectron2")

DISPATCHER_URL = "DISPATCHER_URL_"
TOKEN = "TOKEN_"
bucket = "bucket_"
key = "key_"

config = """CUDNN_BENCHMARK: false
DATALOADER:
  ASPECT_RATIO_GROUPING: true
  FILTER_EMPTY_ANNOTATIONS: false
  NUM_WORKERS: 2
  REPEAT_THRESHOLD: 0.0
  SAMPLER_TRAIN: TrainingSampler
DATASETS:
  PRECOMPUTED_PROPOSAL_TOPK_TEST: 1000
  PRECOMPUTED_PROPOSAL_TOPK_TRAIN: 2000
  PROPOSAL_FILES_TEST: []
  PROPOSAL_FILES_TRAIN: []
  TEST: []
  TRAIN: [dataset]
GLOBAL:
  HACK: 1.0
INPUT:
  CROP:
    ENABLED: false
    SIZE:
    - 0.9
    - 0.9
    TYPE: relative_range
  FORMAT: BGR
  MASK_FORMAT: polygon
  MAX_SIZE_TEST: 1333
  MAX_SIZE_TRAIN: 1333
  MIN_SIZE_TEST: 800
  MIN_SIZE_TRAIN:
  - 640
  - 672
  - 704
  - 736
  - 768
  - 800
  MIN_SIZE_TRAIN_SAMPLING: choice
  RANDOM_FLIP: horizontal
MODEL:
  ANCHOR_GENERATOR:
    ANGLES:
    - - -90
      - 0
      - 90
    ASPECT_RATIOS:
    - - 0.5
      - 1.0
      - 2.0
    NAME: DefaultAnchorGenerator
    OFFSET: 0.0
    SIZES:
    - - 32
    - - 64
    - - 128
    - - 256
    - - 512
  BACKBONE:
    FREEZE_AT: 2
    NAME: build_resnet_fpn_backbone
  DEVICE: cuda
  FPN:
    FUSE_TYPE: sum
    IN_FEATURES:
    - res2
    - res3
    - res4
    - res5
    NORM: ''
    OUT_CHANNELS: 256
  KEYPOINT_ON: false
  LOAD_PROPOSALS: false
  MASK_ON: true
  META_ARCHITECTURE: PanopticFPN
  PANOPTIC_FPN:
    COMBINE:
      ENABLED: true
      INSTANCES_CONFIDENCE_THRESH: 0.5
      OVERLAP_THRESH: 0.5
      STUFF_AREA_LIMIT: 4096
    INSTANCE_LOSS_WEIGHT: 1.0
  PIXEL_MEAN:
  - 103.53
  - 116.28
  - 123.675
  PIXEL_STD:
  - 1.0
  - 1.0
  - 1.0
  PROPOSAL_GENERATOR:
    MIN_SIZE: 0
    NAME: RPN
  RESNETS:
    DEFORM_MODULATED: false
    DEFORM_NUM_GROUPS: 1
    DEFORM_ON_PER_STAGE:
    - false
    - false
    - false
    - false
    DEPTH: 101
    NORM: FrozenBN
    NUM_GROUPS: 1
    OUT_FEATURES:
    - res2
    - res3
    - res4
    - res5
    RES2_OUT_CHANNELS: 256
    RES5_DILATION: 1
    STEM_OUT_CHANNELS: 64
    STRIDE_IN_1X1: true
    WIDTH_PER_GROUP: 64
  RETINANET:
    BBOX_REG_LOSS_TYPE: smooth_l1
    BBOX_REG_WEIGHTS: &id002
    - 1.0
    - 1.0
    - 1.0
    - 1.0
    FOCAL_LOSS_ALPHA: 0.25
    FOCAL_LOSS_GAMMA: 2.0
    IN_FEATURES:
    - p3
    - p4
    - p5
    - p6
    - p7
    IOU_LABELS:
    - 0
    - -1
    - 1
    IOU_THRESHOLDS:
    - 0.4
    - 0.5
    NMS_THRESH_TEST: 0.5
    NORM: ''
    NUM_CLASSES: 80
    NUM_CONVS: 4
    PRIOR_PROB: 0.01
    SCORE_THRESH_TEST: 0.05
    SMOOTH_L1_LOSS_BETA: 0.1
    TOPK_CANDIDATES_TEST: 1000
  ROI_BOX_CASCADE_HEAD:
    BBOX_REG_WEIGHTS:
    - &id001
      - 10.0
      - 10.0
      - 5.0
      - 5.0
    - - 20.0
      - 20.0
      - 10.0
      - 10.0
    - - 30.0
      - 30.0
      - 15.0
      - 15.0
    IOUS:
    - 0.5
    - 0.6
    - 0.7
  ROI_BOX_HEAD:
    BBOX_REG_LOSS_TYPE: smooth_l1
    BBOX_REG_LOSS_WEIGHT: 1.0
    BBOX_REG_WEIGHTS: *id001
    CLS_AGNOSTIC_BBOX_REG: false
    CONV_DIM: 256
    FC_DIM: 1024
    FED_LOSS_FREQ_WEIGHT_POWER: 0.5
    FED_LOSS_NUM_CLASSES: 50
    NAME: FastRCNNConvFCHead
    NORM: ''
    NUM_CONV: 0
    NUM_FC: 2
    POOLER_RESOLUTION: 7
    POOLER_SAMPLING_RATIO: 0
    POOLER_TYPE: ROIAlignV2
    SMOOTH_L1_BETA: 0.0
    TRAIN_ON_PRED_BOXES: false
    USE_FED_LOSS: false
    USE_SIGMOID_CE: false
  ROI_HEADS:
    BATCH_SIZE_PER_IMAGE: 128
    IN_FEATURES:
    - p2
    - p3
    - p4
    - p5
    IOU_LABELS:
    - 0
    - 1
    IOU_THRESHOLDS:
    - 0.5
    NAME: StandardROIHeads
    NMS_THRESH_TEST: 0.5
    NUM_CLASSES: 7
    POSITIVE_FRACTION: 0.25
    PROPOSAL_APPEND_GT: true
    SCORE_THRESH_TEST: 0.05
  ROI_KEYPOINT_HEAD:
    CONV_DIMS:
    - 512
    - 512
    - 512
    - 512
    - 512
    - 512
    - 512
    - 512
    LOSS_WEIGHT: 1.0
    MIN_KEYPOINTS_PER_IMAGE: 1
    NAME: KRCNNConvDeconvUpsampleHead
    NORMALIZE_LOSS_BY_VISIBLE_KEYPOINTS: true
    NUM_KEYPOINTS: 17
    POOLER_RESOLUTION: 14
    POOLER_SAMPLING_RATIO: 0
    POOLER_TYPE: ROIAlignV2
  ROI_MASK_HEAD:
    CLS_AGNOSTIC_MASK: false
    CONV_DIM: 256
    NAME: MaskRCNNConvUpsampleHead
    NORM: ''
    NUM_CONV: 4
    POOLER_RESOLUTION: 14
    POOLER_SAMPLING_RATIO: 0
    POOLER_TYPE: ROIAlignV2
  RPN:
    BATCH_SIZE_PER_IMAGE: 256
    BBOX_REG_LOSS_TYPE: smooth_l1
    BBOX_REG_LOSS_WEIGHT: 1.0
    BBOX_REG_WEIGHTS: *id002
    BOUNDARY_THRESH: -1
    CONV_DIMS:
    - -1
    HEAD_NAME: StandardRPNHead
    IN_FEATURES:
    - p2
    - p3
    - p4
    - p5
    - p6
    IOU_LABELS:
    - 0
    - -1
    - 1
    IOU_THRESHOLDS:
    - 0.3
    - 0.7
    LOSS_WEIGHT: 1.0
    NMS_THRESH: 0.7
    POSITIVE_FRACTION: 0.5
    POST_NMS_TOPK_TEST: 1000
    POST_NMS_TOPK_TRAIN: 1000
    PRE_NMS_TOPK_TEST: 1000
    PRE_NMS_TOPK_TRAIN: 2000
    SMOOTH_L1_BETA: 0.0
  SEM_SEG_HEAD:
    COMMON_STRIDE: 4
    CONVS_DIM: 128
    IGNORE_VALUE: 255
    IN_FEATURES:
    - p2
    - p3
    - p4
    - p5
    LOSS_WEIGHT: 0.5
    NAME: SemSegFPNHead
    NORM: GN
    NUM_CLASSES: 54
  WEIGHTS: https://dl.fbaipublicfiles.com/detectron2/COCO-PanopticSegmentation/panoptic_fpn_R_101_3x/139514519/model_final_cafdb1.pkl
OUTPUT_DIR: output/dataset
SEED: -1
SOLVER:
  AMP:
    ENABLED: false
  BASE_LR: 0.00025
  BASE_LR_END: 0.0
  BIAS_LR_FACTOR: 1.0
  CHECKPOINT_PERIOD: 5000
  CLIP_GRADIENTS:
    CLIP_TYPE: value
    CLIP_VALUE: 1.0
    ENABLED: false
    NORM_TYPE: 2.0
  GAMMA: 0.1
  IMS_PER_BATCH: 2
  LR_SCHEDULER_NAME: WarmupMultiStepLR
  MAX_ITER: 300
  MOMENTUM: 0.9
  NESTEROV: false
  NUM_DECAYS: 3
  REFERENCE_WORLD_SIZE: 0
  RESCALE_INTERVAL: false
  STEPS: []
  WARMUP_FACTOR: 0.001
  WARMUP_ITERS: 1000
  WARMUP_METHOD: linear
  WEIGHT_DECAY: 0.0001
  WEIGHT_DECAY_BIAS: null
  WEIGHT_DECAY_NORM: 0.0
TEST:
  AUG:
    ENABLED: false
    FLIP: true
    MAX_SIZE: 4000
    MIN_SIZES:
    - 400
    - 500
    - 600
    - 700
    - 800
    - 900
    - 1000
    - 1100
    - 1200
  DETECTIONS_PER_IMAGE: 100
  EVAL_PERIOD: 0
  EXPECTED_RESULTS: []
  KEYPOINT_OKS_SIGMAS: []
  PRECISE_BN:
    ENABLED: false
    NUM_ITER: 200
VERSION: 2
VIS_PERIOD: 0"""

model_path = "/vol/cache/"

def download_models():
    import oloren as olo
    
    model_path = olo.download_from_file_record({
        "reserved": "file",
        "bucket": bucket,
        "key": key
    }, dispatcher_url = DISPATCHER_URL, token = TOKEN)
    # gracefully handle the case where the directory already exists
    os.makedirs("/vol/cache", exist_ok=True)
    
    os.system("mv {} /vol/cache/model_final.pth".format(model_path))

image = (
    modal.Image.debian_slim(python_version="3.10")
        .pip_install("oloren")
        .pip_install("Pillow")
        .apt_install("git")
        .pip_install("torch")
        .pip_install("git+https://github.com/facebookresearch/detectron2.git")
        .pip_install("torchvision")
        .pip_install("opencv-python")
        .apt_install("libgl1-mesa-glx")
        .apt_install("libglib2.0-0")
        .run_function(download_models)
)

stub.image = image

@stub.cls(gpu="a10g")
class Detectron2:
    def __enter__(self):
        print( "Entering")
        from detectron2 import model_zoo
        from detectron2.engine import DefaultPredictor
        from detectron2.config import get_cfg
        from detectron2.utils.visualizer import Visualizer
        from detectron2.data import MetadataCatalog, DatasetCatalog
        with open("config.yaml", "w") as f:
            f.write(config)
            
        cfg = get_cfg()
        cfg.merge_from_file("config.yaml")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # set threshold for this model
        cfg.MODEL.WEIGHTS = "/vol/cache/model_final.pth"
        self.predictor = DefaultPredictor(cfg)

    @modal.method()
    def predict(self, img_data_in):
        import cv2
        with open("img", "wb") as f:
            f.write(img_data_in)
        # Read png from input
        image = cv2.imread("img")
        # Make prediction
        output = self.predictor(image)
        
        instances = output["instances"].to("cpu")
        instances_json = {}
        instances_json["pred_boxes"] = instances.pred_boxes.tensor.tolist()
        instances_json["scores"] = instances.scores.tolist()
        instances_json["pred_classes"] = instances.pred_classes.tolist()
        
        return instances_json
    
@stub.local_entrypoint()
def entrypoint(
    image
):
    d2 = Detectron2()
    
    with open(image, "rb") as f:
        image = f.read()
    results = d2.predict.call(image)
    print(results)
    with open("results.json", "w+") as f:
        f.write(json.dumps(results))
        
        
    