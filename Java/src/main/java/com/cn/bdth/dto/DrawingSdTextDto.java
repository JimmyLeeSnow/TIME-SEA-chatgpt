package com.cn.bdth.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.experimental.Accessors;

/**
 * 添加文生图
 *
 * @author 时间海 @github dulaiduwang003
 * @version 1.0
 */
@Data
@Accessors(chain = true)
@SuppressWarnings("all")
public class DrawingSdTextDto {

    @NotBlank(message = "提示词不能为空")
    private String prompt;

    @NotNull(message = "图片宽度不能为空")
    private Long width;

    @NotNull(message = "图片高度不能为空")
    private Long height;

    @NotBlank(message = "模型名称不能为空")
    private String modelName;

    @NotBlank(message = "采样率不能为空")
    private String rate;

    @NotNull(message = "迭代步数不能为空")
    private Integer steps;

    private String negative_prompt;
}
